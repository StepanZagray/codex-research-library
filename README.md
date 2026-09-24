# Codex Research Library

A local-first Codex plugin for bounded, source-grounded research and durable knowledge.

The `$research` skill retrieves existing knowledge before searching, chooses the smallest sufficient research lane, follows claims back to authoritative sources, verifies decision-critical conclusions, and publishes only reusable findings. Delegation is optional and limited to one layer; agents never count as evidence.

The default library path is `~/Research`. Set `RESEARCH_LIBRARY_PATH` to use another location.

## Library model

```text
Research/
├── HOME.md
├── INDEX.md
├── <category>/
│   ├── INDEX.md
│   └── <scope>/
│       ├── INDEX.md
│       └── <topic>.md
└── _runs/
    └── timestamp-topic/
        ├── brief.md
        ├── manifest.json
        ├── findings/
        ├── verification.md
        └── synthesis.md
```

Canonical notes hold the shortest maintained understanding. Runs preserve the brief, raw evidence, verification, and synthesis needed to audit or supersede it.

The plugin uses ordinary Markdown, JSON, and `rg`; it needs no daemon, scheduler, database, vector store, or cloud runtime.

## Contents

- `skills/research/SKILL.md` — lane selection and research workflow.
- `skills/research/references/research-contract.md` — evidence, verification, lifecycle, and publication rules.
- `skills/research/assets/` — run and library templates.
- `skills/research/scripts/start_run.py` — deterministic run initialization.
- `skills/research/scripts/add_assignment.py` — append an assignment, such as an experiment card, to an open run.
- `skills/research/scripts/validate_run.py` — run lifecycle validation.
- `skills/ml-lab/SKILL.md` — orchestrator for ML model development: charter, question loop, experiment cards, role dispatch, and the research library as lab notebook.
- `skills/ml-experiment/SKILL.md` — worker that runs one experiment card: preflight, launch, monitoring, analysis, and the record.
- `skills/ml-experiment/assets/experiment-record.md` — experiment card and record template, compatible with research findings.
- `skills/ml-experiment/references/debugging.md` — diagnosis playbook for models that don't learn.
