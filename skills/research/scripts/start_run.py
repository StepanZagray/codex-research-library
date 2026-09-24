#!/usr/bin/env python3
"""Create a bounded research run with a valid brief, manifest, and finding stubs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def slug(value: str) -> str:
    if not SLUG.fullmatch(value):
        raise argparse.ArgumentTypeError(
            "use lowercase hyphenated text (letters, digits, and single hyphens)"
        )
    return value


def assignment(value: str) -> tuple[str, str]:
    assignment_id, separator, question = value.partition("=")
    if not separator or not question.strip():
        raise argparse.ArgumentTypeError("use ID=QUESTION")
    return slug(assignment_id), question.strip()


def atomic_write(path: Path, content: str) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def finding_stub(title: str) -> str:
    return f"""# {title}

## Answer

Pending.

## Findings

### Finding title

- Status: tentative
- Confidence: low
- Claim:
- Evidence:
- Source tier:
- Source:
- Source date or revision:
- Retrieved:
- Applicability:
- Limits:

## Contradictions and gaps

Pending.

## Search record

- Queries or local retrieval terms:
- Sources rejected and why:
- Stop reason:
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", required=True, type=Path)
    parser.add_argument("--slug", required=True, type=slug)
    parser.add_argument("--question", required=True)
    parser.add_argument("--decision-use", required=True)
    parser.add_argument("--category", required=True, type=slug)
    parser.add_argument("--scope", type=slug)
    parser.add_argument(
        "--in-scope", default="Defined by the question and coverage matrix."
    )
    parser.add_argument(
        "--excluded", default="Unrelated claims and implementation work."
    )
    parser.add_argument(
        "--freshness",
        default="Current as of the run date unless a claim specifies otherwise.",
    )
    parser.add_argument(
        "--source-standard",
        default="Owning primary sources; secondary sources only for discovery or interpretation.",
    )
    parser.add_argument(
        "--search-budget",
        default="Bounded by the completion criterion; record any extension and its reason.",
    )
    parser.add_argument("--completion", required=True)
    parser.add_argument(
        "--stop-condition",
        default="Stop after three unproductive search or hypothesis rounds, or when required evidence is inaccessible.",
    )
    parser.add_argument(
        "--assignment",
        action="append",
        default=[],
        type=assignment,
        metavar="ID=QUESTION",
    )
    parser.add_argument(
        "--timestamp",
        help="UTC timestamp in YYYY-MM-DDTHHMMSSZ form; intended for deterministic tests.",
    )
    args = parser.parse_args()

    library = args.library.expanduser().resolve()
    if not library.is_dir():
        parser.error(f"library does not exist: {library}")
    if not (library / "INDEX.md").is_file():
        parser.error(f"library has no INDEX.md: {library}")

    if args.timestamp:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{6}Z", args.timestamp):
            parser.error("--timestamp must use YYYY-MM-DDTHHMMSSZ")
        run_time = datetime.strptime(args.timestamp, "%Y-%m-%dT%H%M%SZ").replace(
            tzinfo=timezone.utc
        )
    else:
        run_time = datetime.now(timezone.utc).replace(microsecond=0)
    run_stamp = run_time.strftime("%Y-%m-%dT%H%M%SZ")

    assignments = [
        {"id": item_id, "question": question, "status": "pending"}
        for item_id, question in args.assignment
    ]
    if len({item["id"] for item in assignments}) != len(assignments):
        parser.error("assignment IDs must be unique")

    run_id = f"{run_stamp}-{args.slug}"
    run_dir = library / "_runs" / run_id
    findings_dir = run_dir / "findings"
    try:
        findings_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.error(f"run already exists: {run_dir}")

    iso_now = run_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = {
        "id": run_id,
        "question": args.question,
        "decision_use": args.decision_use,
        "category": args.category,
        "scope": args.scope,
        "status": "planning",
        "outcome": "pending",
        "created_at": iso_now,
        "updated_at": iso_now,
        "assignments": assignments,
        "verification": "pending",
        "published_to": None,
        "publication": {"status": "pending", "path": None, "reason": None},
    }

    assignment_lines = (
        "\n".join(f"- `{item['id']}`: {item['question']}" for item in assignments)
        or "- `direct`: Research directly; no delegation is required."
    )
    brief = f"""# Research brief

- Question: {args.question}
- Intended decision or use: {args.decision_use}
- Category: {args.category}
- Scope: {args.scope or "none"}
- In scope: {args.in_scope}
- Excluded: {args.excluded}
- Freshness requirement: {args.freshness}
- Source standard: {args.source_standard}
- Search budget: {args.search_budget}
- Completion criterion: {args.completion}
- Stop or escalation conditions: {args.stop_condition}

## Existing knowledge

Record established, stale, contradictory, and missing knowledge after searching the library.

## Claim and coverage matrix

| Claim or subquestion | Why it matters | Required evidence | Best source owner | Freshness | Status |
|---|---|---|---|---|---|

## Assignments

{assignment_lines}
"""

    atomic_write(run_dir / "brief.md", brief)
    atomic_write(run_dir / "manifest.json", json.dumps(manifest, indent=2) + "\n")
    for item in assignments:
        atomic_write(findings_dir / f"{item['id']}.md", finding_stub(item["question"]))

    print(run_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
