# Aborted setup attempt

An editing command used the wrong working-directory-relative path and failed before applying the runner repair. Its following shell line unintentionally started the old runner. This attempt was stopped during unchanged-baseline preflight after verifying its process IDs and owned temporary server/profile. No mutation results were produced. It is excluded from the experimental denominator, not counted as passed or killed. The subsequent timestamped run uses the repaired runner.
