# Policy-Grounded Agent — Design Memo

**Approach.** A Python CLI processes the conversation turn by turn. A model extracts intents and source-quoted facts; local retrieval loads the governing rules and KB articles; a reviewed, deterministic policy gate makes the decision and computes amounts; bounded templates render the reply. Each turn exposes the retrieved excerpts (with line numbers), governing policy IDs, missing checks, raw model candidate, gate corrections, and final decision. Customer statements never become backend verification, and no real credit or human handoff is executed. Reviewers can use the CLI (`./run.sh replay --offline`) or a local web console (`frontend/` over `scripts/web_api.py`). The console has live chat, transcript replay, and recorded-run views, and shows the same per-turn evidence and gate corrections without duplicating policy logic. Screenshots are in `docs/screenshots/`.

**Fully grounded replies.** (1) The credit amount: Rule 3 and KB-1004/1005 give $225 ÷ 30 × 11 = **$82.50**. The $225 already covers all three lines, so it is not multiplied again. (2) The $75 question: Rule 3 is an explicit exception, so the Rule 2 goodwill ceiling does not apply. Rules 4/5 still govern escalation. (3) The deadline: 30 calendar days from outage restoration, not the 60-day statement window; the request is on day 14. The NOC confirmation is the historical agent's transcript statement, labeled as such, not a new lookup.

**Not grounded, deliberately.** (1) Taxes and surcharges: KB-1004 says the formula uses the recurring plan charge, and KB-1003 describes taxes. No rule says whether a credit recalculates them. The workflow says so and asks for human clarification instead of guessing. (2) Issuance: fraud and dispute-history checks never appear in the conversation, so the action stays pending verification and no approval is claimed. Full-day counting and half-up rounding are documented implementation conventions.

**Hardest part of the hierarchy.** A narrow exception replaces one general rule (the $75 cap) but not the global ones (Rule 4 thresholds, Rule 5 repeat/fraud review). The gate therefore keeps eligibility, arithmetic, and action authority separate, and treats "unknown" as distinct from "false". No ticket, an unverifiable ticket, and an unchecked ticket lead to different paths. A known conservative choice: outage requests also carry Rule 1 invoice-dispute prerequisites, which fits this conversation but can over-hold a pure outage request.

**Model selection: no configuration met the gate; best observed is Claude Sonnet 5.5, adaptive thinking, medium effort.** The rule was fixed in advance: zero critical failures and full mandatory-escalation recall as gates, then success, then turn P95/P50, then cost. Each model + effort setting was scored separately, capped at high. A 22-configuration screen across five families did not discriminate (all 3/3). On 24 development cases, Claude configurations tied at 23/24 versus 21–22/24 for GPT. Final comparison: same pinned workflow-v8 code, fresh blind-authored 16 cases × 3 = 48 per configuration:

| Config | Success | Critical | Escalation | Technical failures |
|---|---|---|---|---|
| Sonnet medium | **44/48** | **1** | **23/24** | 4 contract (8 connection errors rerun) |
| Haiku medium | 34/48 | 6 | 18/24 | 7 contract |
| Sonnet high | 29/48 | 6 | 13/24 | 8 contract + 11 connection |
| Opus high | 25/48 | 12 | 11/24 | 19 contract + 4 connection |
| GPT-6.1 Sol low | 24/48 | 12 | 12/24 | 21 contract |
| Opus medium | 19/48 | 11 | 6/24 | 16 contract + 13 connection |

Every critical failure was a fail-closed contract rejection ("no credit issued, request human assistance"), never a wrong amount or policy. No configuration made an unsupported tax claim. Connection errors came from 16-way concurrent runs, so those rows are infrastructure-confounded. Higher effort did not help. Sonnet medium costs about $0.03–0.045 per conversation (~15× Haiku, the committed development default) at a ~11 s turn P50. On the current workflow-v11, one live replay of the supplied conversation with Sonnet medium passed all six turns with zero technical failures (17 calls, ≈$0.17). An earlier v10 replay with Haiku failed on turn 4. Full record: `docs/model_selection.md`.

**Measuring instruction-following and hallucination continuously.** Freeze code, prompts, corpus, configuration, and oracle hashes per run. Re-run the supplied conversation, then a development regression, then a fresh held-out cohort scored by someone who did not tune the prompts. Report raw-model and post-gate correctness separately:
- Instruction-following: governing-policy accuracy, amount accuracy, mandatory-escalation recall, and over-refusal.
- Hallucination: unsupported claims (citations whose quotes are not in the cited source, invented tax or approval outcomes).

Also track technical fail-closed rate, turn P50/P95, and cost per successful conversation, keeping failures in the denominator. Sample live traffic weekly for human adjudication of semantic disagreements that closed oracles miss. The next concrete step is fresh V3 acceptance on frozen v11 for Sonnet medium and Haiku medium. Main open risks: the 8% fail-closed rate on the understanding contract, intents the model omits entirely, and bill-item aliases without an authoritative ID. A finite suite is not proof of zero hallucination.
