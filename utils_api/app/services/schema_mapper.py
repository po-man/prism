import json
from pathlib import Path
from typing import Any, Dict, List

from app.services.schema_loader import get_schema_path


def load_key_mapping(mapping_file: str = "key_mapping.json") -> Dict[str, str]:
    """Loads the key mapping file from the schemas directory."""
    try:
        # The mapping file is expected to be in the same directory as the schemas.
        # We can derive its path from a known schema path.
        base_path = get_schema_path("v1/impact.schema.json").parent
        mapping_path = base_path / mapping_file
        with open(mapping_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        # If the mapping is missing or corrupt, we can proceed without it,
        # but no keys will be reversed. Log this for debugging.
        print(f"Warning: Could not load key mapping file '{mapping_file}'. Reason: {e}")
        return {}


def reverse_extracted_keys(data: Any, mapping: Dict[str, str]) -> Any:
    """
    Recursively traverses a payload and replaces abbreviated keys with their
    canonical long-form names based on the provided mapping.
    """
    if isinstance(data, dict):
        # Create a new dictionary to avoid issues with changing keys during iteration.
        new_dict = {}
        for key, value in data.items():
            # Determine the new key: use the mapping if available, otherwise keep the original.
            new_key = mapping.get(key, key)
            # Recurse on the value with the same mapping.
            new_dict[new_key] = reverse_extracted_keys(value, mapping)
        return new_dict
    elif isinstance(data, list):
        # If it's a list, apply the reversal to each item in the list.
        return [reverse_extracted_keys(item, mapping) for item in data]
    else:
        # For all other data types (strings, numbers, booleans, null), return the value as is.
        return data