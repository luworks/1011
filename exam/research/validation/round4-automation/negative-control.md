# Round 4 negative controls

Server: Playwright default `npm run dev -- --hostname 127.0.0.1 --port 3100`, `PW_CHANNEL=chrome`, workers=1.
Baseline before mutations (LAY-002 x2, CONTENT-001 x2, CMP-001 /connectors x2): 6 passed, 0 failed (`nc-baseline.log`).
Each mutated file was copied to a scratch backup, mutated, tested, restored with `cp`, and verified byte-identical with `cmp`.

| Control | Mutation | Test filter | Mutated | Restored |
|---|---|---|---|---|
| (a) LAY-002 | `src/app/agents/page.tsx`: inline `<style>{'main h1{font-size:40px}'}</style>` before the list PageHeader | `LAY-002` | 0 passed / 2 failed ("h1 typography on /agents differs from /files") | 2 passed / 0 failed |
| (b) CONTENT-001 | `src/lib/data.ts`: Slack description replaced with Chinese text | `CONTENT-001` | 0 passed / 2 failed ("CJK copy in main on /connectors without data-source-lang") | 2 passed / 0 failed |
| (c) CMP-001 | `src/app/connectors/page.tsx`: `aria-selected={tab === key \|\| index === 2}` (second selected tab) | `CMP-001] /connectors` | 0 passed / 2 failed (selected-tab count expected 1) | 2 passed / 0 failed |

Logs: `nc-a-mutated.log`, `nc-a-restored.log`, `nc-b-*.log`, `nc-c-*.log`.

Full gate after restore: typecheck, lint, test:design (13 pass / 0 fail), check:design (0 violations), build all exit 0;
`PW_CHANNEL=chrome PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:e2e`: 58 passed, 0 failed (`test-e2e.log`).
