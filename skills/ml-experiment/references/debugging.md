# Debugging a model that doesn't learn

Work from the cheapest suspect to the most expensive: **data → labels → pipeline → objective → optimization → architecture → evaluation**. Most "architecture problems" turn out to be data or label problems, and those are cheaper to check.

## First moves, always

1. **Look at the data.** Render a few dozen training inputs with their labels overlaid. Read them as the model would.
2. **Check the loss at initialization.** A K-way classifier should start near `ln K`. A far-off value means a masking, scaling, or label bug.
3. **Overfit one batch.** Train on a single batch until the loss is near zero. If it can't, the problem is in the code, not the data or the scale.
4. **Fit training before validation.** A slice that can't fit its own training data has no validation problem yet.
5. **Compute trivial baselines** for every metric: chance, majority class, copy the input or previous frame, a random valid action. A number means nothing without its baseline.

## Symptoms and suspects

| Symptom | Suspects, cheapest first | Discriminating check |
|---|---|---|
| Loss flat from step 0 | Learning rate, frozen or detached parameters, loss masked to nothing, labels disconnected from inputs | Per-layer gradient norms; overfit one batch; shuffle the labels, and the loss should stay the same |
| Training improves, validation gets worse | Too few *distinct* instances (count unique layouts or levels, not rows); arbitrary tie-breaks in the teacher; shortcuts through absolute position or action history | Count unique instances; measure how many equally good answers each state has; blank a suspected shortcut input and watch validation |
| Plateau somewhat above chance | The needed information isn't reachable: receptive field, resolution (tiny objects inside patch tokens), a pooled bottleneck | Train a small dedicated probe on the same inputs. If the probe succeeds, the information is there and the architecture or objective is the limit |
| One slice flat while others learn | Interference from another slice: conflicting label meanings, poor label quality in another slice, too little exposure | Leave-one-slice-out arms at small scale, run concurrently; audit label quality per slice |
| Late sudden improvement | Normal phase transition, not a failure | Set the kill step past the known takeoff step; use training fit and per-slice metrics as early signals |
| Offline metrics good, closed-loop play fails | Compounding errors off the demonstrated states, repeated-state loops, deterministic tie-breaking, action budget | Trace failed episodes step by step; classify each failure mode and count them before fixing any |
| Metrics swing between evaluations | Eval set too small, seed variance, learning rate too high | Compute a binomial interval or seed spread; enlarge the eval panel before reading trends |
| A fix "works" | Changed conditions, not the fix | Rerun the baseline under the same conditions: code, data version, budget, contention |

## Imitation and teacher labels

When labels come from a teacher or solver:

- **Label every equally good action,** not the teacher's single pick. An arbitrary pick can only be memorized.
- **Check what the teacher can't provide:** states it can't label, moves it never shows (fatal moves), and suboptimal teachers the model will copy.
- **Audit per slice:** fallback-label rate, rollout length, how far through the task each rollout gets.

## Discipline

- One change per test. Keep a single command that reproduces the failure.
- Write the hypothesis before looking at the result.
- After three hypotheses fail in a row, report to the PI what was ruled out and wait for the next card.
