# Release checklist

## Scientific and execution evidence

- [x] Baseline batch, CSTR, and PFR reference completed.
- [x] Temperature-response case completed and accepted.
- [x] First-order analytical and conservation case passed.
- [x] Negative-concentration input was rejected.
- [x] Compact evidence is committed under `results/reference-runs/` and documented in `RUNS.md`.
- [x] Remote compute was assessed as scientifically inapplicable to the ideal local ODE baseline.
- [x] Final packaged quickstart and full notebook rerun completed after the last content edit.

## Repository and release quality

- [x] Tests pass from the documented environment.
- [x] Source compilation and schema checks pass.
- [x] README, project page, one-page PDF, PNG, notebooks, and RUNS.md report consistent values.
- [x] No secrets, private data, proprietary kinetics, or unsafe procedures are present.
- [x] One-page PNG and PDF were regenerated from committed reference results.
- [x] Supplied Vicena logo hashes match in `assets/` and `docs/assets/`.
- [x] No em dash character appears in repository text or notebook Markdown.
- [x] License, VERSION, CITATION.cff, changelog, description, topics, and final URLs agree.
- [x] Git diff and whitespace checks pass.

## Publication verification

- [x] Remote repository is exactly `vicena-labs/chemical-reactor-digital-twin`.
- [x] Remote commit matches local `main` after the final verification commit is pushed.
- [x] README paths, preview, PDF, project page source, and clone URL were verified.
- [x] Description, topics, homepage, and default branch are verified. The standard MIT `LICENSE` file and public license statement are present; GitHub license API SPDX detection remained pending at publication time.
- [x] No GitHub release tag was requested for this initial repository publication.
