# Getting started

Part of the [Vicena Research Twins collection](https://vicena.ai).

1. Create a Python 3.10 or newer environment.
2. Run `python -m pip install -e .`.
3. Validate the bundled manifests:
   `python scripts/validate_dataset.py datasets/synthetic/reaction_network.yaml schemas/reaction-network.schema.json`
4. Generate data: `python scripts/generate_synthetic_data.py`.
5. Run `python scripts/run_baseline.py`.
6. Open the notebooks in order.

The bundled network is abstract and synthetic. It is safe for software demonstration because it does not map to a real preparation or operating procedure.
