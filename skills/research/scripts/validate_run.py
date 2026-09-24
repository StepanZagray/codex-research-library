#!/usr/bin/env python3
"""Validate a research run's deterministic structure and lifecycle invariants."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RUN_STATES = {
    "planning",
    "researching",
    "verifying",
    "synthesizing",
    "complete",
    "failed",
}
OUTCOMES = {"pending", "done", "done_with_concerns", "blocked", "failed"}
ASSIGNMENT_STATES = {"pending", "in_progress", "complete", "failed", "stale"}
VERIFICATION_STATES = {
    "pending",
    "complete",
    "complete_with_concerns",
    "not_required",
}
PUBLICATION_STATES = {"pending", "published", "not_needed"}
TERMINAL_COMPLETE = {"complete"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_directory", type=Path)
    args = parser.parse_args()

    run_dir = args.run_directory.expanduser().resolve()
    errors: list[str] = []

    for relative in ("brief.md", "manifest.json"):
        if not (run_dir / relative).is_file():
            errors.append(f"missing file: {relative}")
    if not (run_dir / "findings").is_dir():
        errors.append("missing directory: findings")

    manifest_path = run_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        manifest = {}
    except json.JSONDecodeError as error:
        manifest = {}
        errors.append(f"manifest.json is invalid JSON: {error}")

    required = {
        "id",
        "question",
        "decision_use",
        "category",
        "scope",
        "status",
        "outcome",
        "created_at",
        "updated_at",
        "assignments",
        "verification",
        "published_to",
        "publication",
    }
    missing = sorted(required - set(manifest))
    if missing:
        errors.append(f"manifest missing keys: {', '.join(missing)}")

    for key in (
        "id",
        "question",
        "decision_use",
        "category",
        "created_at",
        "updated_at",
    ):
        if not isinstance(manifest.get(key), str) or not manifest.get(key, "").strip():
            errors.append(f"manifest {key} must be a non-empty string")

    if manifest.get("id") != run_dir.name:
        errors.append("manifest id must match the run directory name")
    if manifest.get("status") not in RUN_STATES:
        errors.append(f"invalid run status: {manifest.get('status')!r}")
    if manifest.get("outcome") not in OUTCOMES:
        errors.append(f"invalid outcome: {manifest.get('outcome')!r}")
    if manifest.get("verification") not in VERIFICATION_STATES:
        errors.append(f"invalid verification status: {manifest.get('verification')!r}")

    assignments = manifest.get("assignments", [])
    if not isinstance(assignments, list):
        errors.append("assignments must be a list")
        assignments = []
    assignment_ids: set[str] = set()
    for index, item in enumerate(assignments):
        if not isinstance(item, dict):
            errors.append(f"assignment {index} must be an object")
            continue
        item_id = item.get("id")
        if not item_id:
            errors.append(f"assignment {index} has no id")
        elif item_id in assignment_ids:
            errors.append(f"duplicate assignment id: {item_id}")
        else:
            assignment_ids.add(item_id)
        if item.get("status") not in ASSIGNMENT_STATES:
            errors.append(f"assignment {item_id or index} has invalid status")
        if (
            not isinstance(item.get("question"), str)
            or not item.get("question", "").strip()
        ):
            errors.append(f"assignment {item_id or index} has no question")
        if item.get("status") == "complete":
            finding = run_dir / "findings" / f"{item_id}.md"
            if not finding.is_file():
                errors.append(f"completed assignment has no finding: {item_id}")
            else:
                body = finding.read_text(encoding="utf-8")
                for marker in (
                    "## Answer",
                    "## Findings",
                    "## Contradictions and gaps",
                ):
                    if marker not in body:
                        errors.append(f"finding {item_id} is missing {marker}")

    publication = manifest.get("publication")
    if not isinstance(publication, dict):
        errors.append("publication must be an object")
        publication = {}
    publication_status = publication.get("status")
    if publication_status not in PUBLICATION_STATES:
        errors.append(f"invalid publication status: {publication_status!r}")
    if publication_status == "published" and not publication.get("path"):
        errors.append("published runs must record publication.path")
    if publication_status == "not_needed" and not publication.get("reason"):
        errors.append("not_needed publication must record a reason")

    if manifest.get("status") in TERMINAL_COMPLETE:
        if not (run_dir / "synthesis.md").is_file():
            errors.append("completed run is missing synthesis.md")
        if not (run_dir / "verification.md").is_file():
            errors.append("completed run is missing verification.md")
        if manifest.get("verification") == "pending":
            errors.append("completed run cannot have pending verification")
        active = [
            item.get("id", "<unknown>")
            for item in assignments
            if item.get("status") in {"pending", "in_progress"}
        ]
        if active:
            errors.append(f"completed run has active assignments: {', '.join(active)}")
        if publication_status == "pending":
            errors.append("completed run cannot have pending publication")
        if not manifest.get("published_to"):
            errors.append("completed run must record published_to")
        if publication_status == "published" and manifest.get(
            "published_to"
        ) != publication.get("path"):
            errors.append("published_to must match publication.path")
        if (
            publication_status == "not_needed"
            and manifest.get("published_to") != "synthesis.md"
        ):
            errors.append(
                "not_needed publication must set published_to to synthesis.md"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"valid research run: {run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
