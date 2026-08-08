# Codex Research Library

A local-first Codex plugin for rigorous, reusable research.

The `$research` skill searches an existing global knowledge library, decomposes complex questions into bounded subagent assignments, verifies material claims, and publishes source-backed conclusions to categorized Markdown files.

The default library path is `~/Research/Knowledge`. Set `RESEARCH_LIBRARY_PATH` to use another location.

## Library model

```text
Knowledge/
├── INDEX.md
├── ml/
│   ├── INDEX.md
│   └── tofy/
│       ├── INDEX.md
│       └── topic.md
└── _runs/
    └── timestamp-topic/
        ├── brief.md
        ├── manifest.json
        ├── findings/
        └── synthesis.md
```

Categories are broad domains. Optional scopes group project-specific knowledge inside a category; Tofy research uses `ml/tofy`.

The plugin has no server, scheduler, cloud runtime, database, or vector store. Research runs only while Codex is working, and the resulting library is ordinary Markdown suitable for local search and private Git versioning.

## Contents

- `skills/research/SKILL.md` — orchestration workflow.
- `skills/research/references/research-contract.md` — evidence and publication quality gates.
- `skills/research/assets/` — library and run templates.
