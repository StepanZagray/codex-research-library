# <card-id>: <short title>

## Card

Written by the PI before launch. The prediction is frozen once the run starts.

- Decision: If <outcome>, we <action>; otherwise <action>.
- Hypothesis:
- Prediction:
- Baseline: <named run or arm, same code, data, and eval set>
- Changed variable: <one factor, or one named recipe for an exploratory card>
- Metric:
- Early signal: <what should move, per slice, and by when>
- Noise floor: <seed spread or binomial interval at this eval size; filled at preflight>
- Kill criterion: <condition that stops the run early; larger than the noise floor>
- Budget: <wall-clock and GPU/CPU>
- Rung: seconds | minutes | hours

## Answer

- Result: confirmed | refuted | inconclusive | invalid
- Summary: Result against the prediction in one or two sentences, and the decision it supports.

## Findings

### Finding title

- Status: established | supported | tentative | disputed | obsolete
- Confidence: high | medium | low
- Claim: One bounded claim, no broader than the arms tested.
- Evidence: Numbers against the baseline, with seeds and eval-set size.
- Source tier: local-primary
- Source: <log, metrics file, or eval output path, with line or step locator>
- Source date or revision: <commit and diff hash>
- Retrieved: n/a
- Applicability: <model size, data version, families or slices, rung>
- Limits: <noise, confounds, what was not tested>

## Run provenance

- Commit and diff hash:
- Command:
- Output directory and PID file:
- Dataset version and audit report:
- Hardware and measured accelerator utilization:
- PIDs checked at preflight:
- Smoke run result, peak accelerator memory, and step time:
- Seeds and eval-set size:
- Trivial baselines for the metric:
- Wall-clock and stop reason:

## Contradictions and gaps

Confounds, noise bounds, slices that disagree, incidents during the run, and what this result does not show.
