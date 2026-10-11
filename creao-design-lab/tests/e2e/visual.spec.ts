import { test, expect } from '@playwright/test';
import { arch, platform, release } from 'node:os';

// Integrate under tests/e2e after the baseline source freeze is released.
// A visual runner must explicitly identify its OS/font/browser environment.
// This is a namespace, not proof of environment equality: keep the receipt.
const environment = process.env.VISUAL_ENV;

test.use({
  locale: 'en-US',
  timezoneId: 'America/Los_Angeles',
  colorScheme: 'light',
  reducedMotion: 'reduce',
  deviceScaleFactor: 1,
});

test.beforeEach(async ({ browser, page }, testInfo) => {
  expect(environment, 'Set VISUAL_ENV to a reviewed OS-font-browser baseline environment').toMatch(/^[a-z0-9][a-z0-9._-]+$/);
  const actualEnvironment = `${platform()}-${arch()}-${release()}-chromium-${browser.version()}`;
  expect(environment, 'The visual baseline namespace must match this actual OS/kernel, architecture and browser version').toBe(actualEnvironment);
  testInfo.annotations.push({ type: 'visual-environment', description: actualEnvironment });
  testInfo.annotations.push({ type: 'browser-version', description: browser.version() });
  testInfo.annotations.push({ type: 'browser-channel', description: process.env.PW_CHANNEL || 'bundled-chromium' });
  // No clock-generated rows, API requests or user data belong in these snapshots.
  await page.clock.install({ time: new Date('2026-10-11T17:30:00.000Z') });
});

for (const width of [1280, 390]) {
  test(`[VISUAL-001] Files initial list at ${width}x900`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/files');
    await expect(page.getByRole('heading', { level: 1, name: 'Files', exact: true })).toBeVisible();
    await expect(page.getByTestId('file-item')).toHaveCount(4);
    await expect(page.getByRole('button', { name: 'List view', exact: true })).toHaveAttribute('aria-pressed', 'true');
    await page.evaluate(() => document.fonts.ready);
    await expect(page).toHaveScreenshot([environment!, `files-list-${width}x900.png`], {
      animations: 'disabled', caret: 'hide', fullPage: true, scale: 'css',
      maxDiffPixels: 0, threshold: 0.2,
    });
  });
}

test('[VISUAL-001] Connectors connected empty state at 1280x900', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto('/connectors');
  await page.getByRole('tab', { name: /^Connected(?: \(\d+\))?$/ }).click();
  await expect(page.getByRole('button', { name: 'Browse connectable services', exact: true })).toBeVisible();
  await page.evaluate(() => document.fonts.ready);
  await expect(page).toHaveScreenshot([environment!, 'connectors-connected-empty-1280x900.png'], {
    animations: 'disabled', caret: 'hide', fullPage: true, scale: 'css',
    maxDiffPixels: 0, threshold: 0.2,
  });
});
