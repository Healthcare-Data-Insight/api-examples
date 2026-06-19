from __future__ import annotations

import ast
import keyword
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3] / "openapi" / "components" / "schemas" / "model"
OUT = Path(__file__).resolve().parent / "all_classes.py"
ENUMS_PY = Path(__file__).resolve().parent / "enums.py"

PYTHON_KEYWORDS = set(keyword.kwlist) | {"match", "case", "True", "False", "None"}


def snake_case(name: str) -> str:
    chars: list[str] = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0:
            prev = name[i - 1]
            nxt = name[i + 1] if i + 1 < len(name) else ""
            if prev.islower() or prev.isdigit() or (prev.isupper() and nxt.islower()):
                chars.append("_")
        chars.append(ch.lower() if ch.isalnum() else "_")
    result = "".join(chars).replace("-", "_").replace("/", "_")
    while "__" in result:
        result = result.replace("__", "_")
    result = result.strip("_")
    if result in PYTHON_KEYWORDS:
        result = f"{result}_"
    return result


def schema_name_from_ref(ref: str) -> str:
    return Path(ref).stem


def py_string(value: object) -> str:
    return repr(str(value))


def enum_member_name(value: object, used_names: set[str]) -> str:
    base = "".join(ch if ch.isalnum() else "_" for ch in str(value).upper()).strip("_")
    if not base:
        base = "EMPTY"
    if base[0].isdigit():
        base = f"VALUE_{base}"
    name = base
    suffix = 2
    while name in used_names:
        name = f"{base}_{suffix}"
        suffix += 1
    used_names.add(name)
    return name


def merge_schema(schema: dict) -> dict:
    if "allOf" not in schema:
        return {
            "description": schema.get("description"),
            "properties": schema.get("properties", {}),
            "base_ref": None,
        }

    merged = {
        "description": schema.get("description"),
        "properties": {},
        "base_ref": None,
    }
    for part in schema["allOf"]:
        if "$ref" in part:
            merged["base_ref"] = part["$ref"]
        else:
            merged["description"] = merged["description"] or part.get("description")
            merged["properties"].update(part.get("properties", {}))
    return merged


def load_existing_enums() -> set[str]:
    module = ast.parse(ENUMS_PY.read_text())
    return {
        node.name
        for node in module.body
        if isinstance(node, ast.ClassDef)
    }


def build_type(
        schema: dict,
        existing_enums: set[str],
        used_enums: set[str],
        missing_enums: set[str],
) -> str:
    if "$ref" in schema:
        return schema_name_from_ref(schema["$ref"])
    if "oneOf" in schema:
        return " | ".join(
            sorted(
                {
                    build_type(option, existing_enums, used_enums, missing_enums)
                    for idx, option in enumerate(schema["oneOf"])
                }
            )
        )
    enum_name = schema.get("x-enum-name")
    if enum_name:
        if enum_name in existing_enums:
            used_enums.add(enum_name)
            return enum_name
        missing_enums.add(enum_name)
        return "str"

    schema_type = schema.get("type")
    if schema_type == "array":
        item_schema = schema.get("items", {})
        return f"list[{build_type(item_schema, existing_enums, used_enums, missing_enums)}]"
    if schema_type == "string":
        return "dt.date" if schema.get("format") == "date" else "str"
    if schema_type == "integer":
        return "int"
    if schema_type == "number":
        return "float"
    if schema_type == "boolean":
        return "bool"
    if schema_type == "object":
        return "dict[str, object]"
    return "object"


def resolve_order(merged_schemas: dict[str, dict]) -> list[str]:
    remaining = sorted(merged_schemas)
    ordered: list[str] = []
    while remaining:
        progressed = False
        for name in remaining[:]:
            base_ref = merged_schemas[name]["base_ref"]
            base_name = schema_name_from_ref(base_ref) if base_ref else None
            if base_name is None or base_name in ordered:
                ordered.append(name)
                remaining.remove(name)
                progressed = True
        if not progressed:
            raise RuntimeError(f"Cannot resolve inheritance order for: {', '.join(remaining)}")
    return ordered


def main() -> None:
    schemas = {
        path.stem: yaml.safe_load(path.read_text())
        for path in sorted(ROOT.glob("*.yaml"))
    }
    existing_enums = load_existing_enums()
    merged_schemas = {name: merge_schema(schema) for name, schema in schemas.items()}
    ordered = resolve_order(merged_schemas)

    used_enums: set[str] = set()
    missing_enums: set[str] = set()
    class_blocks: list[str] = []

    for name in ordered:
        merged = merged_schemas[name]
        base_name = schema_name_from_ref(merged["base_ref"]) if merged["base_ref"] else "EdiConverterModel"
        description = merged["description"] or f"OpenAPI schema for {name}."
        lines = [f"class {name}({base_name}):", f"    {py_string(description)}"]

        properties = merged["properties"]

        if not properties:
            lines.append("    pass")
        else:
            for prop_name, prop_schema in properties.items():
                attr_name = snake_case(prop_name)
                attr_type = build_type(prop_schema, existing_enums, used_enums, missing_enums)
                attr_description = prop_schema.get("description") or f"{prop_name}."
                is_array = prop_schema.get("type") == "array"

                if is_array:
                    default_expr = f"Field(default_factory=list, description={py_string(attr_description)})"
                else:
                    attr_type = f"{attr_type} | None"
                    default_expr = f"Field(default=None, description={py_string(attr_description)})"

                lines.append(f"    {attr_name}: {attr_type} = {default_expr}")
                lines.append(f"    {py_string(attr_description)}")

        class_blocks.append("\n".join(lines))

    all_names = ["EdiConverterModel", "to_camel", *sorted(used_enums), *ordered]

    content: list[str] = [
        "from __future__ import annotations",
        "",
        "import datetime as dt",
        "",
        "from pydantic import Field",
        "",
        "from .base import EdiConverterModel, to_camel",
        "",
    ]
    if used_enums:
        content.append(f"from .enums import {', '.join(sorted(used_enums))}")
        content.append("")
    if used_enums:
        content.append("")
    content.extend(class_blocks)
    content.append("")
    content.extend(f"{name}.model_rebuild()" for name in ordered)
    content.append("")
    content.append("__all__ = [")
    content.extend(f"    {py_string(name)}," for name in all_names)
    content.append("]")
    content.append("")

    OUT.write_text("\n".join(content))
    print(f"Wrote {OUT}")
    if missing_enums:
        print("Missing enums in edi_model.enums:")
        for enum_name in sorted(missing_enums):
            print(enum_name)


if __name__ == "__main__":
    main()