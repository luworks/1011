# Independent engineer experiment protocol

This experiment supplements deterministic mutation tests. It is a small local trial, not a statistical claim that guidelines prevent all design regressions.

## Frozen baseline

Start only after the canonical app passes its available baseline checks. Record a SHA-256 inventory of source, style, documentation, policy, checker, test, package and lock files. Copy the baseline into separate local experiment directories, excluding generated output and dependency trees. Dependencies may be shared read-only through a symlink. Each run has a separate Next build directory and server port.

## Shared feature request

Add an Important marker to the Files collection. Users can toggle the marker for each synthetic file and filter to Important files. Preserve search, empty-state recovery, mobile readability, accessible control names, and the existing visual language. Changes are local demonstration state only.

## Two independent conditions

- **Engineer A — guideline available:** Read `AGENTS.md` and `design.md`, then implement using the approved components and CSS. Do not change checks, policy, dependencies or their configuration. Deliver the feature diff and concise self-review.
- **Engineer B — shortcuts:** Implement the same feature in an isolated copy while intentionally taking plausible visual/semantic shortcuts. Do not edit or disable tests, policy, dependencies or checking infrastructure. Record the shortcuts after the implementation. Do not manufacture a compilation error as the negative case.

The evaluator must run the original checks in both copies. An engineer's self-report is not the result. Changes to gate assets invalidate a trial, even if their modified checker reports success.

## Evaluation

1. Check the diff remains within feature implementation files and no original test/gate changed.
2. Run typecheck and build; compilation failure is an invalid implementation, not a design-rule detection.
3. Run the same static and browser gates as the baseline, at an isolated port.
4. Independently verify the new marker interaction and filter using the browser. A design-gate pass does not prove the new feature works.
5. Record gate IDs, command exits, behavioral acceptance, screenshots when available, and manual findings separately.
6. Preserve the first result. Any repair is a second recorded attempt, never an overwritten first pass.

## Limits

Two engineers and one feature cannot measure organization-wide compliance rates. These agents know they are in an experiment, and the shortcut condition is intentionally adversarial. Report it as a bounded simulation. The deterministic mutation denominator is separate from this experiment's two implementations.
