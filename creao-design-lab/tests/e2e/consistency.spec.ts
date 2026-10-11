import { test, expect } from '@playwright/test';

test.beforeEach(async ({ browser }, testInfo) => {
  testInfo.annotations.push({ type: 'browser-version', description: browser.version() });
  testInfo.annotations.push({ type: 'browser-channel', description: process.env.PW_CHANNEL || 'bundled-chromium' });
});

const headerRoutes = ['/files', '/connectors', '/agents', '/guidelines'];
const copyRoutes = ['/connectors', '/files'];

for (const width of [1280, 390]) {
  test(`[LAY-002] page header anatomy is consistent across routes at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    const styles: Record<string, { fontFamily: string; fontSize: string; fontWeight: string }> = {};
    for (const route of headerRoutes) {
      await page.goto(route);
      const heading = page.getByRole('main').getByRole('heading', { level: 1 });
      await expect(heading).toHaveCount(1);
      await expect(heading).toBeVisible();
      styles[route] = await heading.evaluate(element => {
        const computed = getComputedStyle(element);
        return { fontFamily: computed.fontFamily, fontSize: computed.fontSize, fontWeight: computed.fontWeight };
      });
    }
    const reference = styles[headerRoutes[0]];
    for (const route of headerRoutes) {
      expect(styles[route], `h1 typography on ${route} differs from ${headerRoutes[0]}`).toEqual(reference);
    }
  });

  test(`[CONTENT-001] collection copy matches document locale at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    for (const route of copyRoutes) {
      await page.goto(route);
      const main = page.getByRole('main');
      await expect(main.getByRole('heading', { level: 1 })).toBeVisible();
      const lang = await page.evaluate(() => document.documentElement.lang);
      expect(lang, `document lang on ${route}`).toMatch(/^en/i);
      // Collect visible text nodes in main; text inside an element marked data-source-lang is an accepted fallback.
      const offenders = await main.evaluate(root => {
        const cjk = /[㐀-鿿]/;
        const found: string[] = [];
        const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
        for (let node = walker.nextNode(); node; node = walker.nextNode()) {
          const text = node.textContent || '';
          if (!cjk.test(text)) continue;
          const parent = node.parentElement;
          if (!parent || parent.closest('[data-source-lang]')) continue;
          const style = getComputedStyle(parent);
          if (style.display === 'none' || style.visibility === 'hidden' || parent.getClientRects().length === 0) continue;
          found.push(text.trim());
        }
        return found;
      });
      expect(offenders, `CJK copy in main on ${route} without data-source-lang`).toEqual([]);
    }
  });
}
