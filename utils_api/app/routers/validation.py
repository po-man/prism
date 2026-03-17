import json
from fastapi import APIRouter, HTTPException
from jsonschema import validate, ValidationError

from app.schemas.validation import ValidationRequest
from app.services.schema_mapper import load_key_mapping, reverse_extracted_keys
from app.services.schema_loader import load_schema

router = APIRouter()


@router.post("/normalize", tags=["Validation"])
async def normalize_data(request: ValidationRequest):
    """
    Normalizes a JSON payload by reversing abbreviated keys and then validates
    it against the specified canonical JSON schema.
    """
    # 1. Load the key mapping and reverse the keys in the payload
    key_mapping = load_key_mapping()
    normalized_data = reverse_extracted_keys(request.data, key_mapping)

    return normalized_data


@router.post("/validate", tags=["Validation"])
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
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/health", tags=["Health"])
async def health_check():
    """A simple health check endpoint."""
    return {"status": "ok"}