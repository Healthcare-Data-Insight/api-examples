# Generate Python EDI Model

Generate python EDI model from OpenAPI spec in openapi/components/schemas/model.

Use pydantic library and strong typing.

Create a class for each object in the OpenAPI spec, all classes reside in the edi_model.all_classes module.
The base class is EdiConverterModel defined in the edi_model.base.

That is, import the EdiConverterModel class from edi_model.base:

```python
from .base import EdiConverterModel, to_camel
```

Map all types accordingly.
Pay attention to the "format" attribute. E.g., use Python date class when the format is "date".
Ignore the "required" attribute and the "default" attributes.
Create enums if the OpenAPI spec defines them.
Create comments (docstrings) for each class and field based on descriptions in the OpenAPI spec. Also, create descriptions for each field using Pydantic's Field class.

## Acceptance Criteria

Run py_compile for all generated/updated files.
Run generate_837p_edi, make sure it runs without errors and returns 200 status code with the EDI string.