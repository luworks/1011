# Human exceptions and scoped bypass

Version: 2026-10-11. This document defines the target contract for human exceptions; the main thread is responsible for CI, the approval adapter, and test integration. Without actual run evidence, this contract must not be labeled as an enabled remote release capability. The existing DS-001/DS-002 exact-file waivers in `exceptions.json` remain the legacy interface; do not write the extended fields below directly into its legacy schema.

## Principles and applicability

By default the system offers a compliant fix recommendation, but allows an owner to explicitly accept a known design deviation for an important feature, a time-boxed experiment, a rule false positive, or a genuine product trade-off. Engineers do not need to repeatedly persuade the agent; once a valid approval exists, the coordinator should carry out the in-scope release and not ask again for the same approval.

A human bypass is a bounded release-acceptance decision: it does not delete failures, turn off the whole QA suite, modify screenshot baselines, or rewrite waived checks as passing. The final status is `accepted_with_exceptions`, distinct from `passed`. The rule itself does not become optional, nor does the approval automatically extend to all later commits.

Allowed scope: explicit instances of layout, component/token usage, copy/recovery flow, and accessibility rules, plus human-reviewed visual differences. Browser/axe/visual findings should not be permanently excluded from the exception process. Each item must state user impact and substitute verification; exceptions that seriously affect core operations or accessibility go through the emergency approval tier.

Design exceptions cannot erase: invalid approval source, mismatched scope or target, rewritten records, expiry/revocation, non-executable build, missing report, browser failed to start, target state not executed, unknown additional failures. These should be reported as `rejected`, `blocked`, or `not_verified`, not as design rules passing. If the release owner still decides to ship under unverified conditions, that is a separately and explicitly recorded release decision; it cannot be passed off as this design gate completing, nor can an engineer/agent presume that authorization.

## Who requests, who approves

| Role | Authority |
| --- | --- |
| Engineer / coding agent | Run checks, prepare requests, give fix recommendations and trade-offs; cannot self-fill an approver identity to complete authorization |
| Coordinator | Aggregate evidence, generate copyable approval wording, validate approvals, run in-scope re-verification, and report; cannot accept risk on a human's behalf |
| Product Design owner / formally delegated design lead | Approve the product rationale of page pattern, visual, and component/token deviations |
| Frontend owner / formally delegated technical lead | Verify impact scope, substitute verification, rollback, and fix plan; standard exceptions require sign-off for both the design and technical responsibilities; a registered person holding both roles may cover both |
| CTO / explicitly registered release owner | May approve emergency exceptions and accept residual design risk for major feature releases; explains why the recommended fix is not adopted and assigns follow-up design/engineering review |

The standard flow does not accept self-approval by the requester. In the emergency flow, the configured release owner makes an explicit decision; if that owner is also the requester, `selfApproval=true`, the emergency rationale, and an independent post-hoc review owner must be recorded; the identity overlap cannot be hidden, and ordinary engineers do not automatically gain equivalent authority.

Role mapping comes from protected configuration and platform identity, not from arbitrary strings in a PR. Before real identities are configured, only local fixture rehearsals are possible, outputting `approvalMode=simulation`; these cannot be used for remote candidates or to claim real approval.

## Scope, time limits, and invalidation

- **Standard exception:** default maximum 7 days; the approval record must give an exact UTC time. **Emergency exception:** maximum 24 hours, naming the post-hoc review owner and deadline. Longer needs should be re-reviewed as a formal pattern/rule change and cannot be renewed indefinitely.
- Bind to one repository, one full `targetSha`, the original check `runId` and evidence digest, the rule/test version, and the request content digest. Local experiments without a commit bind `sourceManifestDigest` and are labeled simulation; do not fabricate a SHA.
- Scope lists specific `ruleId`, `checkId`, and observed finding fingerprints; static issues include the exact file, runtime issues include route/state/viewport; visual issues include the original baseline and diff digest. `*`, whole-repo, all-failures, and unlimited scopes are prohibited.
- Each finding is matched independently. Approving only DS-001 does not waive DS-002 in the same file; a newly appearing unnamed button on the same route is not released because the page already has a visual exception.
- A new commit, changes to the request text, rule version/evidence changes, approval revocation, or expiry invalidate the decision. A re-run may reference the original approval only when the target and request are the same, the evidence can be re-validated, and the approval explicitly allows re-verification of the same candidate; new failures still need handling.
- Renewal is a new approval event; keep the old record and do not rewrite the original expiry. Validity is re-checked at merge/candidate generation and before release. Expiry after deployment is flagged by the inspector for remediation; it does not unilaterally perform rollback or production changes.

## Coordinator operations and human wording

The following are **coordination protocol instructions**, not claims of existing shell/CLI commands. The integration owner must map them to actual tools and record the real invocation in the README; do not run npm scripts that do not exist.

1. `REQUEST_DESIGN_EXCEPTION <request-id>`: read this failure, first present the recommended fix, impact, substitute verification, target identity, and duration; generate a request pending approval.
2. `APPROVE_DESIGN_EXCEPTION <request-id>`: may only be made by a verified authorized person; the approval content must bind the request digest and scope. On receipt, the coordinator verifies identity and the complete record, and does not treat the text token as a secret passphrase.
3. `EVALUATE_DESIGN_EXCEPTION <request-id>`: run/read the complete trusted results of the original checks for the same candidate, then merge approval records with actual findings; output `passed`, `accepted_with_exceptions`, `rejected`, or `blocked`.
4. `REVOKE_DESIGN_EXCEPTION <request-id>`: revoked by an authorized owner; the next candidate/release decision re-checks immediately; historical acceptance results and the revocation event are kept.

When human judgment is needed, the coordinator provides the following concrete template filled with real observed values; it cannot ask a person for a vague "continue":

> As [verified role], I approve design exception [request-id], request digest [request digest], applicable only to [rule/check + file or route/state/viewport + finding fingerprint] in [repository + target SHA]. I have reviewed [run ID + evidence digest] and the recommended fix, and for [business rationale] accept [specific user impact], compensated by [completed substitute verification]. Valid until [UTC timestamp]; [owner] will handle it in [tracking item], using [rollback plan] if needed. This does not approve new failures, other commits, modified tests, or automatic visual baseline updates. The coordinator may run the exception evaluation within this scope without asking again for this approval.

Emergency template additionally:

> This is an emergency, maximum 24 hours, with risk accepted by [CTO/release owner]; the reason for not adopting the regular fix is [reason]; the independent post-hoc reviewer is [reviewer], review deadline [time]; requester and approver are the same person: [true/false].

Engineers can submit the request ID, target SHA, and evidence run via CI dispatch/UI; the request itself is not an approval. CI/QA failure output should provide the wording above and the request entry point, and tell the coordinator which field/approval role is missing, rather than showing only a generic red light.

## Request and audit records

The new mechanism should use separate `governance/release-exceptions/` request records and report receipts, keeping the legacy `exceptions.json` compatible; the final path/schema follows the version tested by the implementation owner. The following fields are an acceptance contract, not the legacy schema:

| Record | Required content |
| --- | --- |
| Request | id, standard/emergency, reason, requestedBy, riskOwner, repository, targetSha or simulation manifest, scope, requestDigest, evidenceRunId/evidenceDigest, policyDigest, requestedExpiry |
| Risk/verification | User impact, recommended fix, why it is not adopted for now, substitute verification and receipt, rollback plan, tracking item; for emergencies the post-hoc reviewer/deadline |
| Approval | Platform principal ID, verified role, approval time, final expiry, requestDigest, approval source/event ID, selfApproval flag, revocation status; not just an approvedBy nickname |
| Decision | Original checks status and complete findings, per-item matched/unmatched results, target/rule/environment identity, approval validation result, decision, exception IDs, command exit codes, executor, and time |

Original checker/browser reports are kept read-only; the aggregator produces a new decision artifact. Even if the candidate is allowed to proceed, the report still shows the failure count, accepted count, unaccepted count, and risk owner. Requests, approvals, revocations, renewals, and fixes are independent events and do not overwrite old records.

## CI/QA integration contract

```text
Fixed candidate and trusted rule version
  → original checks run and reports are saved unconditionally
  → all pass: passed
  → deterministic design findings: give recommended fix or request human exception
  → verify platform identity/approval, SHA, scope, evidence, expiry, revocation
  → every failure validly accepted item by item: accepted_with_exceptions
  → any unmatched/new/expired/unauthorized: rejected
  → missing evidence/infrastructure failure/not executable: blocked
```

The final required CI decision gate may accept `passed` or a verified `accepted_with_exceptions`, but the artifact and job summary must clearly distinguish them. Original failing checks are kept; release cannot be achieved by making failing jobs disappear from required checks. The integration owner should coordinate repository protection settings for the final decision check and the original evidence jobs, so that legitimate exceptions are not permanently blocked by the old original required checks.

Collecting failing exit codes in order to continue generating evidence is allowed, but the final aggregator must verify that every required check actually ran and its report is complete. Prohibited: a global `SKIP_DESIGN`, treating whole-job `continue-on-error` as compliance, deleting assertions, auto-updating snapshots, or converting infraError to passed.

Approval may come from a protected GitHub environment/verified platform approval event; it must be proven that the real approving principal meets the required role and independence. Merely declaring an environment name does not prove reviewers are configured; some environments require only one person from the list to approve, which does not automatically satisfy sign-off for two responsibilities. Repository plan, branch, permissions, re-run actor, and real approval events are all verified by the adapter. When external approval is not configured, reject real releases and provide simulation rehearsal results rather than a fake security boundary.

The trusted workflow version and approval mapping for remote jobs cannot be arbitrarily replaced by the PR awaiting approval; the candidate code execution environment has no approval write permission or production secrets. This contract does not request changing remote permissions, disabling security protections, or auto-releasing now.

## Swarm acceptance matrix

All of the following must keep test inputs, original reports, approval fixtures/trusted events, and decisions; schema unit tests alone do not count as end-to-end verified:

1. No exceptions and compliant: passed; no approval and failures: rejected.
2. Standard approval exactly covering a static finding: accepted_with_exceptions, original finding still present.
3. Specific browser/axe findings and human-reviewed visual differences can each be accepted by scope, not only DS-001/DS-002.
4. CTO/release owner emergency approval can accept a reasonable design deviation; an ordinary engineer/agent impersonating that role is rejected.
5. Expired, future approval time, overlong validity, revoked, wrong role, and self-approval not meeting the tier requirement are all rejected.
6. Mismatched SHA, repository, requestDigest, policyDigest, or run/evidence digest are all rejected.
7. Wildcard scope, different rule on the same path, and new failures on the same route with different state/viewport/fingerprint do not inherit approval.
8. A mixed result with one approved and one unapproved item is still rejected; release only when multiple independent valid approvals exactly cover all acceptable items.
9. Missing report, build failure, browser failed to start, tests skipped, duplicate reports, or candidate changes cannot be disguised as verified via an exception.
10. Original failure report digest unchanged before and after approval; renewal/revocation keep history; behavior at the expiry boundary is well defined.
11. Re-evaluating the same candidate with a valid approval needs no repeated human input; a new commit requires re-authorization.
12. Fail closed when the real role adapter is not configured; simulation output cannot satisfy remote candidate conditions.
13. Complete an integration rehearsal on a real isolated implementation that would otherwise fail: "blocked without approval → accepted after approval → blocked again on expiry/new failure"; prove code unchanged and checks not deleted, with only the verified acceptance decision changing.

## Official references

- [GitHub environments and approvals](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments): required reviewers, self-review prevention, and plan boundaries need actual verification.
- [Workflow re-run identity](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs): re-runs use the permissions of the original triggering actor; do not look only at who triggered the re-run.
