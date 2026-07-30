---
name: chemical-reactor-digital-twin
description: Operate and extend the vendor-neutral batch, CSTR, and PFR research twin.
---
# Chemical Reactor Digital Twin

Read AGENTS.md and AGENT_PLAYBOOK.md. Validate input manifests first. Use SI units internally. Reproduce the synthetic baseline and tests before scientific changes. Keep reusable models in src/, stable inputs in schemas or projects, and notebooks as user-facing analysis only. Separate calibration from held-out validation. Report solver diagnostics, conservation, identifiability, uncertainty, and limitations. Never interpret numerical convergence as chemical validity. Never convert optimization results directly into operating recommendations.
