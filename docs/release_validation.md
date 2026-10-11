# Release validation — workflow-v7 preparation checkpoint

This record describes a locally verified package snapshot, not final model selection or live acceptance. It was produced during the 2026-10-11 coordination window. The v7 live replay and latest report refresh are owned by the coordinator; historical examples must not be promoted as validation of this source.

## Exact snapshot

- Tested outer archive: `dist/policy-grounded-agent-prototype.zip`
- Archive SHA256: `d859495428c862a17303137310205f7961c9a10915d71f99917458ae099f9d1b`
- Python source aggregate SHA256: `6e44d9c0ed20ced430b34bbfa0900f68573e22f93a39f775358a8e37efcc61a9`
- `workflow.py` SHA256: `f3df353e02affd6da19f21bebcf3114eee1b645959965ff11237f7216dee8a85`
- Packaged HTML SHA256: `7610d50bfbd1f6031b98d46d13b4c43be0b55f8d274bd52b8a597d3b09768f98`
- Corpus SHA256: `dbb59ca9a429ab22142b76f32c0704dc3477c5e7ff0a33289efc12d700a05a5f`

The aggregate uses sorted `src/policy_agent/*.py`, updating SHA256 with each basename followed by its bytes. It is not a Git commit identifier and does not cover all non-Python inputs. The exact archive hash covers the full tested deliverable.

## Actual checks

| Check | Result |
|---|---|
| Workspace `uv run pytest -q` | 259 passed |
| Package generation including nested-archive credential scan | Passed |
| Outer archive entries | Exactly `agent_prototype.zip` and `design_memo.md` |
| Standalone HTML in inner archive | Present, byte-identical to `report/dist/index.html` at packaging |
| Fresh temporary extraction and `uv sync --frozen` | Passed, Python 3.12.8 |
| Extracted project's full pytest suite | 259 passed |
| Extracted `doctor` | 15 corpus entries; both keys absent; API access not checked |
| Extracted `doctor --matrix config/eval-models-high.json` | 22 configurations |
| Extracted six-turn offline replay | Passed; $82.50, unsupported-tax boundary, 30-day window; no technical errors |

Clean extraction directory: `/var/folders/zr/hp5t3xpd16b9b_vjf10dd4nm0000gn/T/policy-agent-v7-release-o7b5ae8k`.

No API calls were made for these checks. Default `doctor` still sees the legacy 32-entry default matrix; documented paid examples explicitly select the 22-entry at-most-high matrix. Fixture replay proves local determinism and packaging usability, not current-model semantic accuracy. No fresh holdout labels were inspected for tuning.

## Release handoff

README now selects `config/eval-models-high.json` and distinguishes the shared US$70 cumulative ceiling from the model-selection branch's conservative US$25 cumulative cap. Prior costs and reservations remain on one shared ledger.

Final report refresh, v7 live acceptance, and the final ZIP rebuild remain separate coordinator steps. Rebuilding after this checkpoint changes the archive hash. This document is created after the tested archive and should be included on the next rebuild; its recorded hash intentionally identifies the previous tested snapshot rather than attempting a self-referential archive hash.

## Final stage-delivery freeze

The report owner and coordinator froze and browser-checked HTML SHA256 `abfc9b99cc0214b56c9fc8f929e673183eb1bee2fb87ec2e503b3779cd32a908`. This is the immutable 2026-10-11 12:54:59 PDT report checkpoint, with 62/84 screening runs complete. Fresh/high model acceptance remains pending; no final winner or completed all-model acceptance is claimed.

Workspace final suite: **316 passed**. Current workspace workflow hash remains `8ce60a12d3200fc73116d205d5489df6b020c3e58e8424b73c9e5e175e8de88f`; the real v8 replay continues to identify the earlier `2a561f1aa2bcc42d5ef245c473983417dcd90472d53304601f6da9d2ec30b753` frozen source. The stage package includes post-freeze diagnostics without relabeling that historical live run as validation of the new hash.

A final clean-package check follows this documentation freeze: locked installation, full tests, credential-free doctor, six-turn offline replay, required nested archive layout, and byte-identical HTML. Its exact outer ZIP hash is reported in the release handoff rather than embedded in this file (which would make the archive hash self-referential). Earlier hashes above identify earlier checkpoints only.
