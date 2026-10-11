# Policy Agent Console (local demo)

Next.js frontend for the policy-grounded billing agent. All policy logic stays in
the Python package; the frontend only renders turn traces returned by a local
bridge (`scripts/web_api.py`).

## Run

Two terminals from the project root:

```sh
uv run --frozen python scripts/web_api.py   # bridge on http://127.0.0.1:8790
npm --prefix frontend ci                     # first time only
npm --prefix frontend run dev                # UI on http://localhost:3010
```

## Views

- **Live chat** – multi-turn conversation with a real model using keys from `.env`.
  Default model: `anthropic/claude-sonnet-5-5/adaptive/medium`.
- **Transcript replay** – the supplied Dana Whitfield transcript, either the free
  offline fixture or a live model run.
- **Recorded runs** – read-only replay/chat traces under `runs/`.

Click any agent reply to inspect understanding, final decisions, cited evidence,
model candidate vs. policy gate, and fact provenance.

## Bridge settings (env)

| Variable | Default | Purpose |
| --- | --- | --- |
| `WEB_API_PORT` | `8790` | Bridge port (`POLICY_API_ORIGIN` on the Next side) |
| `WEB_DEFAULT_CONFIG` | Sonnet 5.5 adaptive/medium | Preselected model configuration |
| `WEB_LEDGER` | `runs/web-budget.json` | Demo-only cost ledger |
| `WEB_MAX_COST_USD` | `20` | Cap for that ledger |

Web sessions are saved as `runs/web-chat-*` / `runs/web-replay-*`.
