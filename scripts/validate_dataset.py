import sys
from chemical_reactor_twin.io import load_document, validate_document
if len(sys.argv) != 3:
    raise SystemExit("Usage: python scripts/validate_dataset.py DOCUMENT SCHEMA")
validate_document(load_document(sys.argv[1]), sys.argv[2])
print(f"VALID: {sys.argv[1]}")
