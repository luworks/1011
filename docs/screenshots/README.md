# Console screenshots

Captured from the local demo console (`frontend/`, served over `scripts/web_api.py`) on October 11, 2026. No model API calls were made to capture them.

1. `01-offline-replay-turn4-outage-credit.png`: transcript replay (offline fixture), turn 4, the "$75 limit" question. The Inspector shows the final decision ($82.50, grounded, pending verification), governing Rules 1/3/4/5, condition checks, the still-missing fraud and dispute-history checks, and the cited Rule/KB excerpts with line ranges.
2. `02-offline-replay-turn5-tax-escalation.png`: turn 5, the tax and surcharge question. The workflow states the evidence gap and requires human clarification instead of guessing.
3. `03-live-v11-sonnet-replay-turn4.png`: recorded live run `final-replay-sonnet-medium-v11` (workflow-v11, Claude Sonnet 5.5 adaptive/medium, 17 calls, ≈$0.174), turn 4, with the same final decision produced from real model output after the policy gate.
