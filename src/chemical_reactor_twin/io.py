"""Input validation for reaction and experimental manifests."""
import json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

def load_document(path):
    path = Path(path)
    with path.open() as f:
        return yaml.safe_load(f) if path.suffix.lower() in {".yaml", ".yml"} else json.load(f)

def validate_document(document, schema_path):
    schema = load_document(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda e: list(e.path))
    if errors:
        raise ValueError("\n".join(f"{list(e.path)}: {e.message}" for e in errors))
    return True
