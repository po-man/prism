import json
import os
import re
import argparse
from typing import List, Dict, Any

def slugify(text: str) -> str:
    """
    Generates a URL-friendly slug from a string.
    Converts to lowercase, removes non-word characters (except hyphens),
    and replaces spaces with hyphens.
    """
    text = text.lower()
    # Replace '&' with 'and'
    text = re.sub(r'\s*&\s*', '-and-', text)
    # Remove all non-word characters (everything except numbers and letters)
    text = re.sub(r'[^\w\s-]', '', text)
    # Replace all runs of whitespace with a single dash
    text = re.sub(r'\s+', '-', text)
    return text

def create_markdown_stub(org_data: Dict[str, Any]) -> str:
    """
    Creates the markdown front matter content for an organization.
    """
    org_id = org_data.get("id")
    org_name = org_data.get("name")

    if not org_id or not org_name:
        raise ValueError("Organization data must contain 'id' and 'name' keys.")

    slug = slugify(org_name)

    # Using f-string to create the multi-line string for the front matter
    content = f"""---
title: "{org_name}"
data_id: "{org_id}"
type: ""
slug: "{slug}"
---
"""
    return content

def process_directory(input_dir: str, output_dir: str):
    """
    Reads all JSON files in an input directory, generates markdown stubs,
    and writes them to the output directory.
    """
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory not found at {input_dir}")
        return

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    print(f"Found {len(json_files)} JSON files to process in '{input_dir}'.")

    for filename in json_files:
        input_path = os.path.join(input_dir, filename)
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # The JSON file is expected to be a list containing one object
            if isinstance(data, list) and len(data) > 0:
                org_data = data[0]
            else:
                print(f"Warning: Skipping {filename}. Expected a list with one item, but found {type(data)}.")
                continue

            markdown_content = create_markdown_stub(org_data)
            org_id = org_data.get("id")
            if not org_id:
                raise ValueError("'id' key not found in JSON object.")

            output_filename = f"{org_id}.md"
            output_filepath = os.path.join(output_dir, output_filename)

            with open(output_filepath, 'w', encoding='utf-8') as f_out:
                f_out.write(markdown_content)

            print(f"Successfully generated: {output_filepath}")

        except (ValueError, KeyError) as e:
            print(f"Error processing {filename}: {e}")
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {filename}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {filename}: {e}")

def main():
    """Main function to parse arguments and run the script."""
    parser = argparse.ArgumentParser(
        description="Generate Hugo markdown stubs from organization JSON data.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "input_dir",
        help="Path to the input directory containing JSON files (e.g., 'data/organisations/')."
    )
    parser.add_argument(
        "output_dir",
        help="Path to the output directory for markdown files (e.g., 'web/content/')."
    )

    args = parser.parse_args()
    process_directory(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()
