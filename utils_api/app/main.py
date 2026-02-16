import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from jsonschema import validate, ValidationError
from typing import Any, Dict

app = FastAPI()

SCHEMA_DIR = os.getenv("SCHEMA_DIR", "/schemas")

class ValidationRequest(BaseModel):
    schema_name: str
    data: Dict[str, Any]

def load_schema(schema_name: str) -> Dict[str, Any]:
    """Loads a JSON schema from the filesystem."""
    # Basic path traversal protection
    if ".." in schema_name or schema_name.startswith("/"):
        raise FileNotFoundError("Invalid schema path.")

    schema_path = os.path.join(SCHEMA_DIR, schema_name)
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema '{schema_name}' not found at '{schema_path}'.")

    with open(schema_path, 'r') as f:
        return json.load(f)

@app.post("/validate")
async def validate_data(request: ValidationRequest):
    """
    Validates a JSON object against a specified JSON schema.
    """
    try:
        schema = load_schema(request.schema_name)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Schema '{request.schema_name}' is not valid JSON.")

    try:
        validate(instance=request.data, schema=schema)
        return {
            "schema": request.schema_name,
            "valid": True,
        }
    except ValidationError as e:
        error_details = {
            "status": "invalid",
            "message": e.message,
            "path": list(e.path),
            "validator": e.validator,
            "validator_value": e.validator_value,
        }
        return {
            "schema": request.schema_name,
            "valid": False,
            "details": error_details
        }
    except Exception as e:
        # Catch other potential errors during validation
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/health")
async def health_check():
    """
    A simple health check endpoint.
    """
    return {"status": "ok"}