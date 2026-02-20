from json_schema_to_pydantic import create_model
from pydantic import BaseModel
from typing import Type

from app.services.schema_loader import load_schema


def create_dynamic_model(schema_name: str) -> Type[BaseModel]:
    """
    Loads a JSON schema and generates a Pydantic model from it.
    """
    schema = load_schema(schema_name)
    return create_model(schema, allow_undefined_type=True)