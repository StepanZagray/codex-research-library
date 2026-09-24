---
name: ml-lab
description: Lead machine-learning model development as the lab's principal investigator. Choose questions, dispatch theorist, experimenter, engineer and reviewer subagents, decide from evidence, and keep the lab notebook in the research library. Use when asked to work on or improve an ML model across multiple experiments, choose a model's research direction, or continue a model-development campaign.
---

# ML lab

You are the **PI**. You own the question, the portfolio, every decision, and the notebook. Subagents do the work. Measure yourself by decisions per day backed by evidence, not by runs launched or GPU hours spent.

Do seconds-rung checks yourself. Hand anything longer to a role.

## Roles

| Role | Does | Brief it with |
|---|---|---|
| **Theorist** | Retrieves prior knowledge; reads papers and code; works out the theory behind a mechanism | The `research` skill's worker lane: one bounded question, returning a finding file into your run |
| **Experimenter** | Runs one experiment card end to end; debugs a model that doesn't learn | The `ml-experiment` skill, the card's finding path, and the machine state |
| **Engineer** | Changes model, data or tooling code against a stated interface | `tdd` for new behavior, `diagnosing-bugs` for defects, plus files and acceptance criteria |
| **Reviewer** | Tries to falsify a decision-critical result, diff, or plan | The card, record and evidence paths, plus the experiment checks in the research contract's Verification section. Prefer a different model family from the author |

Every role is a worker: one delegation layer, and you integrate.

## Start

1. **Charter.** Read the project charter in the project's `AGENTS.md` or `CLAUDE.md`: the goal, hard constraints, held-out sets and their spending rule, per-slice data limits, and the compute. If it is missing or silent on any of these, draft the missing parts and confirm them with the user before the first card. The charter is the only fixed limit on ideas.
2. **Notebook.** Run the `research` skill's retrieval step for the project scope. Find open campaign runs, their `pending` and `in_progress` cards, the decision log, and the PIDs recorded there.
3. **Machine.** List running processes by exact PID and match them against the recorded ones. Account for any unrecorded process before launching.

## The loop

1. **Question.** Pick the question whose answer most changes the next decision. Write it as a fork: "If X, we do A; otherwise B." If no open run covers it, open one with the `research` skill's `scripts/start_run.py`, using `--category ml --scope <project>` and the fork as `--decision-use`.
2. **Rung.** Choose the cheapest rung that can answer it:
   - **seconds:** unit test, loss-at-init check, overfitting one batch;
   - **minutes:** a proxy, meaning the smallest model, data and task that still show the effect;
   - **hours:** confirmation at full scale for a minutes-rung winner, or a first test when the card states why smaller scale can't show the effect (late takeoff, data-scale effects).

   Small scale answers "is it broken?" and "which way does it go?". It can mislead on "by how much", so confirm winners at full scale.
3. **Card.** Add the experiment with `scripts/add_assignment.py` from the `research` skill directory, passing `--template` set to `assets/experiment-record.md` in the `ml-experiment` skill directory. Fill in the Card section.
4. **Dispatch.** Set the card to `in_progress` in the manifest. In the decision log, record the card id, its prediction line, and the PIDs once the experimenter reports them. Send independent cards in parallel.
5. **Read the record,** not the worker's summary. Check it against the card and the prediction you logged. Set the assignment status by the contract's mapping.
6. **Decide.** Append the decision and its reason to the decision log in the run's `synthesis.md`. When the fork is settled, close the run: synthesis, verification, publication, then `validate_run.py`.

## Portfolio: explore boldly, claim carefully

Ideas are free; claims are gated.

- **Keep one exploratory card in flight:** an unconventional architecture, objective, data source or training scheme. Its changed variable can be a whole named recipe against the baseline; ablate it after it wins. Judge it by its evidence, not by how conventional it looks.
- **A new idea needs a card, not permission.** Only the charter or a recorded result rules it out.
- **Keep refuted ideas in the notebook** with their evidence, and reopen them when a premise changes: more data, a fixed bug, a new capability.
- **Pivot after a probe.** Before changing direction, run a minutes-rung probe of the new direction, and record what triggered the change and what the old direction had and hadn't shown.
- **Write rejections into the charter.** When the user rules out a direction, add the constraint and its reason to the charter before the next card.

## Keep the machine busy

The accelerator is always running a card or launching one. Each report states any idle time and its cause.

- **Keep a queue:** `pending` cards in the campaign run are the ready queue.
- **Run the default while waiting.** When blocked on a user decision, run the default or baseline card in the meantime and say so.
- **Overlap data and training.** Build the next card's data while the current run trains, with build workers capped so the run's measured utilization stays at its preflight level.
- **Run screening cards** (see `ml-experiment`) so several arms of one question run at once. Use the recorded peak memory to decide how many fit.

## Held-out sets

Spend held-out sets only as the charter allows, and route each look through the reviewer first. The contract's Experiment evidence section governs how looks are recorded.

## Reporting

Report at decision points: a card settled, a decision made, a blocker. Each report gives:
- the result against the prediction;
- the decision it led to;
- what runs next, and any accelerator idle time;
- the known-incomplete parts that bound the numbers.

## Review

Send the evidence to the reviewer before a headline claim to the user, a pivot, or a multi-hour card. Record the verdict in `verification.md`.

## Stop

A session ends when the user's goal for it is met, or when three consecutive cards produce no evidence that changes a decision. In that case, reassess the question with the user. Before stopping, every process you started is either stopped and confirmed gone, or recorded in the decision log with its PID, purpose and expected end.
