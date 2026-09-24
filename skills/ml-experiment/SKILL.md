---
name: ml-experiment
description: Run one ML experiment card end to end (preflight, smoke test, launch, monitor against its kill criterion, analyze, write the experiment record), or diagnose a model that trains but doesn't learn. Use when dispatched with an experiment card, asked to run a single training, evaluation, or ablation, or asked why a model fails to learn, overfits, plateaus, or fails in closed-loop use.
---

# ML experiment

You run one **card** and return an **experiment record** the PI can decide from. The record is done when it has a result class, the result compared against the frozen prediction, and every number next to the path it came from.

**Dispatched by `ml-lab`:** you are a worker. The record path is a finding file in the PI's research run, with the Card section already filled in. Write the rest of that file and nothing else in the research library. Scripts and configs for this card are yours. Changes to shared model, data or library code go back to the PI as an engineer request, unless the card authorizes them. Do the work yourself rather than dispatching further agents.

**Standalone:** copy [`assets/experiment-record.md`](assets/experiment-record.md) into the run's output directory and fill in the Card section yourself first.

## 1. Read the card

Every Card field must be filled. Fill missing ones from the brief and mark them "set by experimenter". Once the run starts, the prediction is frozen.

The changed variable is one factor, or for an exploratory card one named recipe against the baseline. If the card mixes several unnamed changes, report back before launching.

## 2. Preflight

Preflight is done when each item below has its line in Run provenance. Each item is a failure that has already happened:

- **Code:** the intended change is actually in the tree. Diff it and record the commit and diff hash.
- **Device:** the training process itself reports the accelerator. Print the device from inside the process; environment variables can be changed by imports.
- **Machine:** nothing else is running on the accelerator, and the CPU is free enough to feed it. Record the exact PIDs you checked.
- **Data:** the dataset passed its audit (see Data gate). Record its version.
- **Smoke run:** a tiny run reaches its first evaluation and checkpoint save end to end. Record peak accelerator memory and step time.
- **Throughput:** loader workers are on, and a one- to two-minute check shows the accelerator busy. Fix low utilization, or record it, before the long run.
- **Baselines and noise floor:** compute trivial baselines on the same eval set, and the noise floor at this eval-set size and seed count (binomial interval or seed spread). A prediction or kill criterion smaller than the noise floor goes back to the PI.

## 3. Launch

Use the project's launcher when one exists. Otherwise record the command, write the PID to `<out>/pid`, report the PID to the PI, and note the log path and start time. Every run gets its own output directory; report files carry the run's name so runs can't overwrite each other. Size timeouts to the budget, allowing for contention.

## 4. Monitor

Watch the card's early signal and kill criterion per slice, as well as the headline metric. A slice that stays flat, or one whose arrival drags others down, counts as a kill trigger when the card says so. Report upward only at a trigger: kill criterion hit, prediction clearly settled, crash, budget reached.

When the kill criterion hits, stop. Extend only if the card allows it. Stop processes by the exact PID in the PID file and confirm `/proc/<pid>` is gone; name patterns also match your own shell and your wait-scripts.

## 5. Analyze

- **Baseline:** compare against it under the same code, data version, eval set and budget.
- **Noise:** compare the difference with the noise floor from preflight.
- **Slices:** break results down per slice (task, family, class, level). Aggregates hide a slice that is flat.
- **Training and validation:** report both. Training fit comes first.
- **Result class:**
  - `confirmed` / `refuted`: the prediction held or failed, beyond the noise floor.
  - `inconclusive`: inside the noise floor, or the budget ended before the early signal could appear.
  - `invalid`: a bug, leakage, wrong code or wrong data. The record stays as an incident, and its numbers are never cited as evidence.

If the model trains but doesn't learn what the card expected, work through [`references/debugging.md`](references/debugging.md) before proposing a fix. It is ordered cheapest suspect first and maps symptoms to discriminating checks.

## 6. Record and return

Fill in the record: Answer, Findings (evidence packets, source tier `local-primary`), Run provenance, and Contradictions and gaps. Checkpoints, logs and datasets stay in the project; the record cites them by path, commit and version.

Your final message to the PI gives:
- the result class, and the result against the prediction in one line;
- the record path;
- processes still running, with their PIDs, or "none";
- peak memory and step time, which the PI uses to decide how many arms fit at once;
- anything that could invalidate the result.

## Data gate

A dataset is a versioned artifact, built in three steps:

1. **Smoke build:** a few items per slice, in minutes.
2. **Audit:** counts per slice; coverage (for example, how far through each task rollouts get); label-quality rates (fallbacks, ambiguous labels, failures); duplicates and leakage between splits; and a rendered sample of inputs with labels. Check each slice against the per-slice limits from the charter or card. With no limit given, flag any slice whose fallback or failure rate exceeds 10%.
3. **Full build** into a new version directory, with the audit report stored alongside it.

A slice outside its limits is excluded, or flagged on the card before training uses it.

## Screening cards

A screening card compares several arms cheaply. Shrink model width, batch size and data until the arms fit the accelerator together, using the smoke run's peak memory. Arms share seeds and differ in exactly one variable each. Screening results pick which arms get a confirmation card.
