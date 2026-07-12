#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PACKAGE_VERSION="$(
python - <<'PY'
import tomllib

with open("pyproject.toml", "rb") as pyproject_file:
    print(tomllib.load(pyproject_file)["project"]["version"])
PY
)"

WHEEL_PATH="dist/ediconvert_sdk-${PACKAGE_VERSION}-py3-none-any.whl"

echo "Cleaning previous build artifacts..."
rm -rf build dist ./*.egg-info src/*.egg-info

echo "Building ediconvert-sdk ${PACKAGE_VERSION}..."
python -m build --no-isolation

if python -c "import twine" >/dev/null 2>&1; then
    echo "Checking package metadata with twine..."
    python -m twine check dist/*
else
    echo "Skipping twine check because twine is not installed."
fi

echo "Installing built wheel non-editably..."
python -m pip install --force-reinstall --no-deps "$WHEEL_PATH"

echo "Verifying installed package import locations..."
python - <<'PY'
import pathlib
import sys
from importlib import metadata

import edi_model
import ediconvert_sdk

api_dir = pathlib.Path(__file__).resolve().parent
for module in (ediconvert_sdk, edi_model):
    module_path = pathlib.Path(module.__file__).resolve()
    print(f"{module.__name__}: {module_path}")
    if api_dir in module_path.parents:
        raise SystemExit(
            f"{module.__name__} imported from the source tree instead of the installed wheel"
        )

distribution = metadata.distribution("ediconvert-sdk")
distribution_path = pathlib.Path(str(distribution._path)).resolve()
print(f"ediconvert-sdk metadata: {distribution.version} ({distribution_path})")
if api_dir in distribution_path.parents:
    raise SystemExit(
        "ediconvert-sdk metadata resolved from the source tree instead of the installed wheel"
    )
print(f"python: {sys.executable}")
PY

echo "Running Python API example suite..."
python -m pytest "$SCRIPT_DIR/test_python_api_scripts.py"
