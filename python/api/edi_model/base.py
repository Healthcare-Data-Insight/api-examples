from enum import Enum

from pydantic import BaseModel, ConfigDict
from pydantic_core import core_schema


def to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class EdiConverterModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    def __str__(self) -> str:
        data = self.model_dump(exclude_none=True)
        return data.__str__()
        # return json.dumps(data, indent=2)

    def __repr__(self) -> str:
        return self.__str__()


class EdiEnumOld(Enum):
    def __new__(cls, code):
        obj = object.__new__(cls)
        obj._value_ = code
        return obj

    @property
    def code(self):
        return self.value

    @classmethod
    def from_code(cls, code):
        return cls(code)

    def __str__(self):
        return self.code


class EdiEnum(Enum):
    """
    Base enum for cases like:
      HEIGHT = ("HT", None)

    Behavior:
    - enum.value -> "HT"         (EDI code)
    - enum.name  -> "HEIGHT"     (symbolic name)
    - enum.desc  -> optional description
    - Pydantic input accepts enum names, e.g. "HEIGHT"
    - Pydantic output emits enum names, e.g. "HEIGHT"
    """

    def __new__(cls, code: str):
        obj = object.__new__(cls)
        obj._value_ = code
        return obj

    @property
    def code(self) -> str:
        return self.value

    @classmethod
    def from_code(cls, code: str):
        return cls(code)

    @classmethod
    def from_name(cls, name: str):
        try:
            return cls[name]
        except KeyError:
            raise ValueError(
                f"Unknown {cls.__name__} name: {name}. "
                f"Expected one of: {', '.join(cls.__members__.keys())}"
            )

    @classmethod
    def _validate_for_pydantic(cls, v):
        if isinstance(v, cls):
            return v

        if isinstance(v, str):
            # Accept enum name first
            if v in cls.__members__:
                return cls[v]

            # Optional: also accept raw EDI code
            try:
                return cls(v)
            except ValueError:
                pass

        raise ValueError(
            f"Invalid {cls.__name__}: {v!r}. "
            f"Expected enum name or code."
        )

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.no_info_after_validator_function(
            cls._validate_for_pydantic,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: v.name
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema_, handler):
        json_schema = handler(core_schema_)
        json_schema.update(
            type="string",
            enum=list(cls.__members__.keys()),
            examples=[next(iter(cls.__members__.keys()))] if cls.__members__ else [],
        )
        return json_schema