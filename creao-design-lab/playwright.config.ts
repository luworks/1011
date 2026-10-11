import { defineConfig, devices } from '@playwright/test';

const baseURL = process.env.BASE_URL || 'http://127.0.0.1:3100';
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: [['list'], ['json', { outputFile: process.env.PLAYWRIGHT_JSON_OUTPUT_NAME || 'reports/e2e.json' }]],
  use: { ...devices['Desktop Chrome'], channel: process.env.PW_CHANNEL || undefined, baseURL, trace: 'retain-on-failure', screenshot: 'only-on-failure' },
  webServer: process.env.PW_EXTERNAL_SERVER === '1' ? undefined : {
    command: process.env.PW_SERVER_COMMAND || 'npm run dev -- --hostname 127.0.0.1 --port 3100',
    url: baseURL,
    reuseExistingServer: false,
    timeout: 120_000,
    cwd: __dirname,
  },
});
