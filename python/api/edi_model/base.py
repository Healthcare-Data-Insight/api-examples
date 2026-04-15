from pydantic import BaseModel, ConfigDict


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