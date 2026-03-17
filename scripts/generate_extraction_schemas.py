import json
import os
from pathlib import Path

# Configuration for fields to be pruned from the extraction schemas.
# These fields are populated by downstream processes, not by the LLM.
# Paths are dot-separated keys to navigate the schema dictionary.
FIELDS_TO_PRUNE = [
    "definitions.source.properties.resolved_url",
    "properties.currency.properties.usd_exchange_rate",
    "properties.currency.properties.rate_date",
]


class PruningError(Exception):
    """Custom exception for schema pruning errors."""

def humanize_key(key: str) -> str:
    """Converts a snake_case key to a human-readable Title Case string."""
    return key.replace("_", " ").title()


def process_node(node, key_mapping):
    """
    Recursively traverses a JSON schema node (dict or list) and applies transformations.

    - Flattens enums into string types with descriptions.
    - Shortens property keys using 'x-extract-key' and updates descriptions.
    - Populates the key_mapping dictionary.
    """
    if isinstance(node, dict):
        # 1. Handle enum transformation at the current level
        if "enum" in node:
            enum_values = node.pop("enum")
            node["type"] = "string"
            description = node.get("description", "")
            allowed_values_str = f"[ALLOWED VALUES: {', '.join(map(repr, enum_values))}]"
            node["description"] = f"{description} {allowed_values_str}".strip()
        
        # 2. Handle semantic key shortening within a 'properties' object
        if "properties" in node and isinstance(node["properties"], dict):
            properties = node["properties"]
            # Use a list of keys to handle dictionary size changes during iteration
            for original_key in list(properties.keys()):
                prop_value = properties.get(original_key)
                
                if isinstance(prop_value, dict) and "x-extract-key" in prop_value:
                    short_key = prop_value.pop("x-extract-key")
                    original_description = prop_value.get("description", "")
                    humanized_original_key = humanize_key(original_key)
                    
                    # Prepend the humanized original key to the description
                    prop_value["description"] = f"{humanized_original_key}: {original_description}"
                    
                    # Add mapping and swap the key in the properties object
                    key_mapping[short_key] = original_key
                    properties[short_key] = prop_value
                    del properties[original_key]
                    
                    # CRITICAL FIX: Update the 'required' array if it exists
                    if "required" in node and isinstance(node["required"], list):
                        if original_key in node["required"]:
                            node["required"].remove(original_key)
                            node["required"].append(short_key)
        
        # 3. Recurse into all child values of the dictionary
        for value in node.values():
            # Recurse into the value
            process_node(value, key_mapping)

    elif isinstance(node, list):
        for item in node:
            process_node(item, key_mapping)

    return node


def prune_fields(schema: dict, paths_to_prune: list[str]):
    """
    Prunes specified fields from a schema dictionary based on a list of dot-separated paths.

    Args:
        schema: The schema dictionary to modify.
        paths_to_prune: A list of strings, where each string is a dot-separated path to a field to remove.
    """
    for path_str in paths_to_prune:
        path_parts = path_str.split('.')
        field_to_remove = path_parts[-1]
        parent_path_parts = path_parts[:-1]

        # Navigate to the parent dictionary
        try:
            parent_node = schema
            for part in parent_path_parts:
                parent_node = parent_node[part]
        except KeyError:
            # Path does not exist in this schema, which is acceptable.
            continue

        # Prune the field if it exists
        if isinstance(parent_node, dict) and field_to_remove in parent_node:
            del parent_node[field_to_remove]
            print(f"  - Pruned '{path_str}'")

            # Also remove it from the parent's 'required' array, if present
            grandparent_path_parts = path_parts[:-2]
            grandparent_node = schema
            for part in grandparent_path_parts:
                grandparent_node = grandparent_node[part]
            if "required" in grandparent_node and isinstance(grandparent_node["required"], list) and field_to_remove in grandparent_node["required"]:
                grandparent_node["required"].remove(field_to_remove)

def generate_extraction_schemas(source_dir: Path, output_dir: Path):
    """
    Generates lightweight extraction schemas from canonical validation schemas.
    """
    if not source_dir.exists():
        print(f"Error: Source directory not found at '{source_dir}'")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    key_mapping = {}

    # Find all canonical schemas, excluding any existing extraction schemas
    schema_files = [f for f in source_dir.glob("*.schema.json") if not f.name.endswith(".extract.schema.json")]

    for schema_path in schema_files:
        print(f"Processing {schema_path.name}...")
        with open(schema_path, "r") as f:
            schema_data = json.load(f)

        # --- Field Pruning (Configurable) ---
        prune_fields(schema_data, FIELDS_TO_PRUNE)
        # --- AST Traversal and Transformation ---
        transformed_schema = process_node(schema_data, key_mapping)

        # --- Output Extraction Schema ---
        output_filename = schema_path.stem + ".extract.schema.json"
        output_path = output_dir / output_filename
        with open(output_path, "w") as f:
            json.dump(transformed_schema, f, indent=2)
        print(f"  - Generated extraction schema: {output_path.name}")

    # --- Output Key Mapping ---
    mapping_path = output_dir / "key_mapping.json"
    with open(mapping_path, "w") as f:
        # Sort keys for deterministic output
        sorted_mapping = dict(sorted(key_mapping.items()))
        json.dump(sorted_mapping, f, indent=2)
    print(f"\nGenerated key mapping file: {mapping_path.name}")


if __name__ == "__main__":
    # Assuming the script is run from the project root
    project_root = Path(__file__).parent.parent
    schemas_v1_dir = project_root / "schemas" / "v1"

    generate_extraction_schemas(
        source_dir=schemas_v1_dir,
        output_dir=schemas_v1_dir
    )
    print("\nBuild script finished.")