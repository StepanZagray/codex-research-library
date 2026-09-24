#!/usr/bin/env python3
"""Append a pending assignment to an open research run and create its finding file."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from start_run import atomic_write, finding_stub, slug  # noqa: E402

NO_ASSIGNMENTS = "- `direct`: Research directly; no delegation is required."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_directory", type=Path)
    parser.add_argument("--id", required=True, type=slug, dest="assignment_id")
    parser.add_argument("--question", required=True)
    parser.add_argument(
        "--template",
        type=Path,
        help="Finding template, such as the ml-experiment record; "
        "'<card-id>' and '<short title>' are filled in.",
    )
    args = parser.parse_args()

    question = args.question.strip()
    if not question:
        parser.error("--question must not be empty")
    template = args.template.expanduser() if args.template else None
    if template and not template.is_file():
        parser.error(f"template not found: {template}")

    run_dir = args.run_directory.expanduser().resolve()
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.is_file():
        parser.error(f"not a research run: {run_dir}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        parser.error(f"manifest.json is invalid JSON: {error}")
    if manifest.get("status") in {"complete", "failed"}:
        parser.error(f"run is terminal ({manifest['status']}); open a new run")

    assignments = manifest.setdefault("assignments", [])
    if any(item.get("id") == args.assignment_id for item in assignments):
        parser.error(f"assignment already exists: {args.assignment_id}")
    finding = run_dir / "findings" / f"{args.assignment_id}.md"
    if finding.exists():
        parser.error(f"finding file already exists: {finding}")

    if template:
        body = template.read_text(encoding="utf-8")
        body = body.replace("<card-id>", args.assignment_id).replace(
            "<short title>", question
        )
    else:
        body = finding_stub(question)

    assignments.append(
        {"id": args.assignment_id, "question": question, "status": "pending"}
    )
    if manifest.get("status") == "planning":
        manifest["status"] = "researching"
    manifest["updated_at"] = (
        datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    )

    # Manifest first: a failed finding write leaves a retryable state, never an orphan file.
    atomic_write(manifest_path, json.dumps(manifest, indent=2) + "\n")
    finding.parent.mkdir(exist_ok=True)
    atomic_write(finding, body)

    brief_path = run_dir / "brief.md"
    if brief_path.is_file():
        brief = brief_path.read_text(encoding="utf-8")
        line = f"- `{args.assignment_id}`: {question}"
        if NO_ASSIGNMENTS in brief:
            brief = brief.replace(NO_ASSIGNMENTS, line)
        else:
            brief = brief.rstrip("\n") + "\n" + line + "\n"
        atomic_write(brief_path, brief)

    print(finding)
    return 0


if __name__ == "__main__":
    sys.exit(main())
