import os
import json
from functools import lru_cache
from typing import Any, Dict

SCHEMA_DIR = os.getenv("SCHEMA_DIR", "/schemas")

@lru_cache(maxsize=128)
def load_schema(schema_name: str) -> Dict[str, Any]:
    """
    Loads a JSON schema from the filesystem.
    Results are cached to improve performance.
    """
    # Basic path traversal protection
    if ".." in schema_name or schema_name.startswith("/"):
        raise FileNotFoundError("Invalid schema path.")

    schema_path = os.path.join(SCHEMA_DIR, schema_name)
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema '{schema_name}' not found at '{schema_path}'.")

    with open(schema_path, 'r') as f:
        return json.load(f)