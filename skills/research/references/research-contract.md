# Research contract

## Contents

1. [Quality gates](#quality-gates)
2. [Library and run layout](#library-and-run-layout)
3. [Brief and coverage matrix](#brief-and-coverage-matrix)
4. [Source ladder](#source-ladder)
5. [Evidence packets](#evidence-packets)
6. [Experiment evidence](#experiment-evidence)
7. [Verification](#verification)
8. [Synthesis and publication](#synthesis-and-publication)
9. [Run manifest](#run-manifest)
10. [Interruption and maintenance](#interruption-and-maintenance)
11. [Stopping rule](#stopping-rule)

## Quality gates

A research run is complete only when:

1. The brief names an exact question, intended use, scope, exclusions, freshness need, search budget, and completion criterion.
2. Existing library knowledge and relevant incomplete runs were searched first.
3. The weakest decision-critical premise was tested before broad collection.
4. Every material factual claim has traceable evidence and a source locator.
5. The source that owns each claim was used when reasonably accessible.
6. Every final citation target resolves exactly as written and its locator supports the adjacent claim.
7. Decision-critical claims received an adversarial verification verdict.
8. Facts, interpretation, conflicts, uncertainty, source limits, and negative results remain distinguishable.
9. The synthesis answers the brief rather than merely summarizing sources.
10. Publication is either completed or explicitly marked unnecessary with a reason.
11. The run and library pass their validators, and no research process remains active.

Never use the number of sources or agents as a quality proxy. One directly applicable specification can outweigh many derivative articles.

## Library and run layout

```text
<library>/
├── HOME.md                       # optional human-facing map
├── INDEX.md
├── <category>/
│   ├── INDEX.md
│   └── <scope>/                  # optional project or enduring subject
│       ├── INDEX.md
│       └── <topic>.md
└── _runs/
    └── <timestamp>-<topic>/
        ├── brief.md
        ├── manifest.json
        ├── findings/
        │   └── <assignment>.md
        ├── verification.md
        └── synthesis.md
```

Use lowercase hyphenated paths. Categories are broad and stable; scopes group project-specific or enduring subject knowledge. Use `ml/tofy` for Tofy model architecture, training, evaluation, ARC-AGI, and related machine-learning research.

Run files are the evidence and activity layer. Canonical topic notes are maintained knowledge. Do not promote raw worker prose automatically.

## Brief and coverage matrix

Record the brief before broad web searching or delegation:

```markdown
# Research brief

- Question:
- Intended decision or use:
- Category:
- Scope:
- In scope:
- Excluded:
- Freshness requirement:
- Source standard:
- Search budget:
- Completion criterion:
- Stop or escalation conditions:

## Existing knowledge

Established, stale, contradictory, and missing knowledge.

## Claim and coverage matrix

| Claim or subquestion | Why it matters | Required evidence | Best source owner | Freshness | Status |
|---|---|---|---|---|---|

## Assignments

Independent, bounded evidence questions.
```

A search budget may bound query rounds, source count, corpus, date range, runtime, or all of them. It is a guardrail, not a target. Extend it only when a named decision-critical gap remains and record why.

For empirical work, state a falsifiable hypothesis and the cheapest decisive prerequisite check. For comparisons, define the comparator class and the metric or decision rule before reading results.

## Source ladder

Prefer sources in this order:

1. **Local canonical or project evidence.** Current code, configuration, logs, retained artifacts, and maintained topic notes are primary evidence for project-specific behavior.
2. **Owning primary source.** Official documentation, source code, specification, standard, paper, dataset, filing, court text, or first-party record.
3. **Independent primary source.** Use when replication, corroboration, or competing ownership matters.
4. **High-quality secondary source.** Use for discovery, history, comparison, expert interpretation, or claims no primary source can directly establish.
5. **Search snippet or model memory.** Treat only as a lead; never cite as support.

Primary does not mean infallible. Check version, incentives, methodology, population, and applicability. A first-party marketing claim may own what the vendor said but not whether the claim is true.

When an ideal source is inaccessible, record the failed access path, use the best available substitute, narrow the claim, and reduce confidence. Do not silently promote secondary evidence to primary status.

For current topics, verify the latest applicable version and distinguish publication date, event date, and retrieval date. For technical questions, prefer official documentation, specifications, repositories, and papers over tutorials.

## Evidence packets

Use one packet per material claim:

```markdown
### Finding title

- Status: established | supported | tentative | disputed | obsolete
- Confidence: high | medium | low
- Claim: One precise, bounded claim.
- Evidence: What the source directly establishes.
- Source tier: local-primary | owning-primary | independent-primary | secondary
- Source: [Descriptive title](URL) or local path with line, page, section, table, figure, commit, or run locator.
- Source date or revision: YYYY-MM-DD, version, commit, or unknown
- Retrieved: YYYY-MM-DD for web sources
- Applicability: Population, version, environment, jurisdiction, or other supported scope.
- Limits: Missing evidence, assumptions, conflicts, or reasons confidence is not higher.
```

Rules:

- Keep the claim no broader than the evidence.
- Label inference explicitly; a source need not share the interpretation.
- Cite the source that owns the claim, not a search-results page or worker summary.
- Record local paths with enough precision for another agent to reproduce the reading.
- Distinguish absence of evidence from evidence of absence.
- Preserve contradictory and negative evidence.
- Follow copyright and quotation limits; prefer concise paraphrase.
- Reopen every final citation target and check its exact locator before completion; reject mistyped paths, stale redirects, and locators that support only a neighboring claim. Repeat the full resolvable target every time—never emit `...`, “same source,” or another shorthand in place of a URL or path.

## Experiment evidence

An experiment campaign stores ML experiments as assignments. Each finding file is an experiment record in the `ml-experiment` template: a Card section written before launch, then Answer, Findings, Run provenance, and Contradictions and gaps. It keeps the three sections the validator requires. `ml-experiment` defines the result classes; an `invalid` record stays in the run as an incident and is never cited as support.

- **Tier:** experiment results are `local-primary` evidence for claims about this project's code, data, and models. They are not evidence for claims beyond the arms tested.
- **Locators:** cite the log, metrics file, or eval output with its step or line, plus the commit, diff hash, and dataset version. Checkpoints, logs, and datasets stay in the project; the record points to them.
- **Frozen prediction:** the Card's prediction is never edited after launch; the integrator's decision log keeps a copy from dispatch. A changed plan becomes a new card.
- **Scale:** state the rung (seconds, minutes, or hours) in Applicability. A screening result supports a direction, not a headline number.
- **Held-out sets:** record every look at a held-out set in the record that made it. The first look is the headline; label later looks post-investigation.
- **Assignment status:** `pending` means queued; `in_progress` means dispatched; `complete` means a record exists, whatever its result class; `failed` means no record could be written; `stale` means a newer card replaced it.
- **Decision log:** a campaign's `synthesis.md` starts with a `## Decision log` section while the run is open. The integrator appends each dispatch (card id, prediction line, PIDs) and each decision with its reason. The final synthesis sections follow it.

A long program spans several campaign runs, linked from the scope index or a canonical topic note.

## Verification

Give each decision-critical claim one verdict:

- `verified` — directly supported, current enough, and scoped correctly.
- `qualified` — directionally supported but wording, scope, or confidence must narrow.
- `disputed` — credible evidence conflicts and the disagreement affects the answer.
- `unsupported` — the cited evidence does not establish the claim.
- `stale` — the source or claim is no longer current enough.
- `not_verifiable` — the required evidence is inaccessible or does not exist.

Record the verdict, reason, strongest source, shared-source dependencies, and required synthesis change. A verifier must try to falsify, not merely summarize.

For an experiment record, the verifier also tries to invalidate the result: the intended code actually ran; train/eval leakage; baseline under different conditions; a difference within seed or eval-set noise; a confound from a second changed variable; slices that contradict the aggregate. Reproduce the decisive number from the cited artifacts when that's cheap.

Independent agents are independent readers, not independent evidence. Two agents citing the same paper count as one evidentiary line. For high-impact claims, prefer a separate verifier; if unavailable, perform a fresh adversarial pass and disclose that it was not agent-independent.

## Synthesis and publication

Structure the run synthesis as:

```markdown
# Synthesis title

## Answer

The direct answer and decision implication.

## Verified baseline

What owning evidence establishes now.

## Landscape and disagreement

Common, emerging, disputed, or source-dependent positions.

## Interpretation

Explicit reasoning for this question, including assumptions.

## Unknowns and negative results

Material gaps, failed searches, and evidence that did not support the hypothesis.

## Decision and next check

The resulting decision, plus only the next research that could change it.

## Sources

Deduplicated sources with access dates where relevant.
```

Publish a canonical topic note only when the result is durable, novel, or changes maintained knowledge. A useful one-off answer may remain in the completed run with publication marked `not_needed`.

Use this canonical topic shape:

```markdown
---
title: "Topic title"
type: topic
status: current
created: YYYY-MM-DD
updated: YYYY-MM-DD
category: category
scope: optional-scope
tags: [tag]
research_runs: ["relative/run/path"]
---

# Topic title

## Current understanding

The shortest accurate synthesis.

## Established findings

Source-backed findings with citations adjacent to claims.

## Interpretation and decisions

Clearly labeled implications and decisions.

## Disputed or uncertain

Contradictions, weak evidence, and unknowns.

## Sources

Deduplicated source list.
```

Update an existing topic in place rather than creating a near-duplicate. Preserve prior run references. Mark superseded conclusions and explain why they changed; never rewrite completed run evidence silently.

## Run manifest

Use JSON with this minimum shape:

```json
{
  "id": "2026-08-19T191737Z-topic",
  "question": "Research question",
  "decision_use": "Decision or deliverable this will inform",
  "category": "knowledge-management",
  "scope": "optional-scope",
  "status": "planning",
  "outcome": "pending",
  "created_at": "2026-08-19T19:17:37Z",
  "updated_at": "2026-08-19T19:17:37Z",
  "assignments": [],
  "verification": "pending",
  "published_to": null,
  "publication": {
    "status": "pending",
    "path": null,
    "reason": null
  }
}
```

Valid run states are `planning`, `researching`, `verifying`, `synthesizing`, `complete`, and `failed`. Use the additive `outcome` field for `pending`, `done`, `done_with_concerns`, `blocked`, or `failed`; this preserves the library's stable lifecycle schema while making the user-facing result explicit. Map a blocked run to `status: failed` and `outcome: blocked`.

Assignment states are `pending`, `in_progress`, `complete`, `failed`, and `stale`. Verification is `pending`, `complete`, `complete_with_concerns`, or `not_required` for a run with no decision-critical claims. Publication status is `pending`, `published`, or `not_needed`.

A completed run must have a synthesis, non-pending verification, only complete assignments, and either:

- `publication.status: published` with the same canonical path in `publication.path` and `published_to`; or
- `publication.status: not_needed` with a reason and `published_to: synthesis.md`, keeping the completed run itself as the durable target.

Use `outcome: blocked` when required evidence or authority is unavailable, and `outcome: failed` for integrity or execution failure. Do not label an incomplete run complete merely because a budget expired.

## Interruption and maintenance

On a later invocation, inspect relevant nonterminal manifests. Resume only when the question, inputs, source policy, and freshness requirement still match. Mark obsolete assignments `stale`; do not silently reuse them.

Canonical maintenance must:

- check referenced files and sources for staleness;
- expose contradictory entries rather than selecting one silently;
- deduplicate topic notes by concept, not filename alone;
- preserve completed evidence referenced by canonical notes;
- record corrections through a new run or dated addendum.

No agent may delete completed evidence merely because a conclusion changed. Uncited temporary intake may be pruned according to the library's own policy.

## Stopping rule

Stop when the completion criterion is met, decision-critical claims have verdicts, and another search round is unlikely to change the answer. Stop earlier when the required evidence is inaccessible and report the gap.

After three unproductive query or hypothesis rounds, stop and reassess the premise, source class, or scope. Continue only when a specific new route could resolve a named material gap. Never search merely to consume a budget or make the report look comprehensive.
