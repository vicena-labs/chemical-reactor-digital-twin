import argparse, json
from .io import load_document, validate_document

def main():
    p = argparse.ArgumentParser(prog="reactor-twin")
    sub = p.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate")
    v.add_argument("document"); v.add_argument("schema")
    args = p.parse_args()
    if args.command == "validate":
        validate_document(load_document(args.document), args.schema)
        print(json.dumps({"valid": True, "document": args.document, "schema": args.schema}))
