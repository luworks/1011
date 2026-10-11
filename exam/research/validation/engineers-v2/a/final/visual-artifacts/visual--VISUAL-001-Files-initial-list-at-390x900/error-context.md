# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: visual.spec.ts >> [VISUAL-001] Files initial list at 390x900
- Location: tests/e2e/visual.spec.ts:29:7

# Error details

```
Error: expect(page).toHaveScreenshot(expected) failed

  9567 pixels (ratio 0.03 of all image pixels) are different.

  Snapshot: darwin-arm64-25.6.0-chromium-154.0.8037.98/files-list-390x900.png

Call log:
  - Expect "toHaveScreenshot(darwin-arm64-25.6.0-chromium-154.0.8037.98/files-list-390x900.png)" with timeout 5000ms
    - verifying given screenshot expectation
  - taking page screenshot
    - disabled all CSS animations
  - waiting for fonts to load...
  - fonts loaded
  - 9567 pixels (ratio 0.03 of all image pixels) are different.
  - waiting 100ms before taking screenshot
  - taking page screenshot
    - disabled all CSS animations
  - waiting for fonts to load...
  - fonts loaded
  - captured a stable screenshot
  - 9567 pixels (ratio 0.03 of all image pixels) are different.

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e2]:
    - link "跳到主要内容" [ref=e3] [cursor=pointer]:
      - /url: "#main-content"
    - generic [ref=e4]:
      - button "切换导航" [ref=e5] [cursor=pointer]
      - generic [ref=e7]: CREAO
    - main [ref=e8]:
      - generic [ref=e9]:
        - heading "文件" [level=1] [ref=e11]
        - button "新建文件夹" [ref=e13] [cursor=pointer]
      - searchbox "搜索文件和文件夹" [ref=e20]
      - generic [ref=e21]:
        - paragraph [ref=e22]: 4 个项目
        - button "只看重要" [ref=e23] [cursor=pointer]
        - group "文件显示方式" [ref=e24]:
          - button "列表视图" [pressed] [ref=e25] [cursor=pointer]
          - button "网格视图" [ref=e27] [cursor=pointer]
      - status [ref=e30]
      - list [ref=e32]:
        - listitem [ref=e33]:
          - generic [ref=e34]:
            - button "季度研究摘要.md" [ref=e39] [cursor=pointer]
            - button "季度研究摘要.md：重要" [ref=e40] [cursor=pointer]: 重要
          - generic [ref=e41]:
            - generic [ref=e42]: 修改时间
            - generic [ref=e43]: 10月11日 10:30
          - generic [ref=e44]:
            - generic [ref=e45]: 大小
            - generic [ref=e46]: 12 KB
          - generic [ref=e47]:
            - generic [ref=e48]: 来源
            - generic [ref=e49]: 演示文件
        - listitem [ref=e50]:
          - generic [ref=e51]:
            - button "产品需求与设计评审记录.md" [ref=e56] [cursor=pointer]
            - button "产品需求与设计评审记录.md：重要" [ref=e57] [cursor=pointer]: 重要
          - generic [ref=e58]:
            - generic [ref=e59]: 修改时间
            - generic [ref=e60]: 10月10日 16:45
          - generic [ref=e61]:
            - generic [ref=e62]: 大小
            - generic [ref=e63]: 24 KB
          - generic [ref=e64]:
            - generic [ref=e65]: 来源
            - generic [ref=e66]: 演示文件
        - listitem [ref=e67]:
          - generic [ref=e68]:
            - button "团队工作空间布局草图.svg" [ref=e74] [cursor=pointer]
            - button "团队工作空间布局草图.svg：重要" [ref=e75] [cursor=pointer]: 重要
          - generic [ref=e76]:
            - generic [ref=e77]: 修改时间
            - generic [ref=e78]: 10月10日 11:20
          - generic [ref=e79]:
            - generic [ref=e80]: 大小
            - generic [ref=e81]: 8 KB
          - generic [ref=e82]:
            - generic [ref=e83]: 来源
            - generic [ref=e84]: 演示文件
        - listitem [ref=e85]:
          - generic [ref=e86]:
            - button "跨团队协作项目的长期研究资料与待确认事项汇总.md" [ref=e91] [cursor=pointer]
            - button "跨团队协作项目的长期研究资料与待确认事项汇总.md：重要" [ref=e92] [cursor=pointer]: 重要
          - generic [ref=e93]:
            - generic [ref=e94]: 修改时间
            - generic [ref=e95]: 10月9日 09:15
          - generic [ref=e96]:
            - generic [ref=e97]: 大小
            - generic [ref=e98]: 32 KB
          - generic [ref=e99]:
            - generic [ref=e100]: 来源
            - generic [ref=e101]: 演示文件
  - alert [ref=e102]
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | import { arch, platform, release } from 'node:os';
  3  | 
  4  | // Integrate under tests/e2e after the baseline source freeze is released.
  5  | // A visual runner must explicitly identify its OS/font/browser environment.
  6  | // This is a namespace, not proof of environment equality: keep the receipt.
  7  | const environment = process.env.VISUAL_ENV;
  8  | 
  9  | test.use({
  10 |   locale: 'zh-CN',
  11 |   timezoneId: 'America/Los_Angeles',
  12 |   colorScheme: 'light',
  13 |   reducedMotion: 'reduce',
  14 |   deviceScaleFactor: 1,
  15 | });
  16 | 
  17 | test.beforeEach(async ({ browser, page }, testInfo) => {
  18 |   expect(environment, 'Set VISUAL_ENV to a reviewed OS-font-browser baseline environment').toMatch(/^[a-z0-9][a-z0-9._-]+$/);
  19 |   const actualEnvironment = `${platform()}-${arch()}-${release()}-chromium-${browser.version()}`;
  20 |   expect(environment, 'The visual baseline namespace must match this actual OS/kernel, architecture and browser version').toBe(actualEnvironment);
  21 |   testInfo.annotations.push({ type: 'visual-environment', description: actualEnvironment });
  22 |   testInfo.annotations.push({ type: 'browser-version', description: browser.version() });
  23 |   testInfo.annotations.push({ type: 'browser-channel', description: process.env.PW_CHANNEL || 'bundled-chromium' });
  24 |   // No clock-generated rows, API requests or user data belong in these snapshots.
  25 |   await page.clock.install({ time: new Date('2026-10-11T17:30:00.000Z') });
  26 | });
  27 | 
  28 | for (const width of [1280, 390]) {
  29 |   test(`[VISUAL-001] Files initial list at ${width}x900`, async ({ page }) => {
  30 |     await page.setViewportSize({ width, height: 900 });
  31 |     await page.goto('/files');
  32 |     await expect(page.getByRole('heading', { level: 1, name: '文件', exact: true })).toBeVisible();
  33 |     await expect(page.getByTestId('file-item')).toHaveCount(4);
  34 |     await expect(page.getByRole('button', { name: '列表视图', exact: true })).toHaveAttribute('aria-pressed', 'true');
  35 |     await page.evaluate(() => document.fonts.ready);
> 36 |     await expect(page).toHaveScreenshot([environment!, `files-list-${width}x900.png`], {
     |                        ^ Error: expect(page).toHaveScreenshot(expected) failed
  37 |       animations: 'disabled', caret: 'hide', fullPage: true, scale: 'css',
  38 |       maxDiffPixels: 0, threshold: 0.2,
  39 |     });
  40 |   });
  41 | }
  42 | 
  43 | test('[VISUAL-001] Connectors connected empty state at 1280x900', async ({ page }) => {
  44 |   await page.setViewportSize({ width: 1280, height: 900 });
  45 |   await page.goto('/connectors');
  46 |   await page.getByRole('tab', { name: /^已连接(?: \(\d+\))?$/ }).click();
  47 |   await expect(page.getByRole('button', { name: '浏览可连接服务', exact: true })).toBeVisible();
  48 |   await page.evaluate(() => document.fonts.ready);
  49 |   await expect(page).toHaveScreenshot([environment!, 'connectors-connected-empty-1280x900.png'], {
  50 |     animations: 'disabled', caret: 'hide', fullPage: true, scale: 'css',
  51 |     maxDiffPixels: 0, threshold: 0.2,
  52 |   });
  53 | });
  54 | 
```