# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: visual.spec.ts >> [VISUAL-001] Files initial list at 1280x900
- Location: tests/e2e/visual.spec.ts:29:7

# Error details

```
Error: expect(page).toHaveScreenshot(expected) failed

  4735 pixels (ratio 0.01 of all image pixels) are different.

  Snapshot: darwin-arm64-25.6.0-chromium-154.0.8037.98/files-list-1280x900.png

Call log:
  - Expect "toHaveScreenshot(darwin-arm64-25.6.0-chromium-154.0.8037.98/files-list-1280x900.png)" with timeout 5000ms
    - verifying given screenshot expectation
  - taking page screenshot
    - disabled all CSS animations
  - waiting for fonts to load...
  - fonts loaded
  - 4735 pixels (ratio 0.01 of all image pixels) are different.
  - waiting 100ms before taking screenshot
  - taking page screenshot
    - disabled all CSS animations
  - waiting for fonts to load...
  - fonts loaded
  - captured a stable screenshot
  - 4735 pixels (ratio 0.01 of all image pixels) are different.

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e2]:
    - link "跳到主要内容" [ref=e3] [cursor=pointer]:
      - /url: "#main-content"
    - complementary [ref=e4]:
      - link "CREAO" [ref=e5] [cursor=pointer]:
        - /url: /files
      - navigation "主要导航" [ref=e6]:
        - link "智能体" [ref=e7] [cursor=pointer]:
          - /url: /agents
        - link "文件" [ref=e11] [cursor=pointer]:
          - /url: /files
        - link "连接器" [ref=e16] [cursor=pointer]:
          - /url: /connectors
        - link "设计规范" [ref=e19] [cursor=pointer]:
          - /url: /guidelines
      - generic [ref=e22]:
        - generic [ref=e23]: C
        - generic [ref=e24]:
          - text: 本地交互原型
          - generic [ref=e25]: CREAO Design Lab
    - main [ref=e26]:
      - generic [ref=e27]:
        - heading "文件" [level=1] [ref=e29]
        - button "新建文件夹" [ref=e31] [cursor=pointer]
      - searchbox "搜索文件和文件夹" [ref=e38]
      - generic [ref=e39]:
        - paragraph [ref=e40]: 4 个项目
        - group "文件显示方式" [ref=e41]:
          - button "列表视图" [pressed] [ref=e42] [cursor=pointer]
          - button "网格视图" [ref=e44] [cursor=pointer]
      - status [ref=e47]
      - generic [ref=e48]:
        - generic [aria-hidden] [ref=e49]:
          - generic [ref=e50]: 名称
          - generic [ref=e51]: 修改时间
          - generic [ref=e52]: 大小
          - generic [ref=e53]: 来源
        - list [ref=e54]:
          - listitem [ref=e55]:
            - button "季度研究摘要.md" [ref=e61] [cursor=pointer]
            - generic [ref=e62]: 10月11日 10:30
            - generic [ref=e63]: 12 KB
            - generic [ref=e64]: 演示文件
          - listitem [ref=e65]:
            - button "产品需求与设计评审记录.md" [ref=e71] [cursor=pointer]
            - generic [ref=e72]: 10月10日 16:45
            - generic [ref=e73]: 24 KB
            - generic [ref=e74]: 演示文件
          - listitem [ref=e75]:
            - button "团队工作空间布局草图.svg" [ref=e82] [cursor=pointer]
            - generic [ref=e83]: 10月10日 11:20
            - generic [ref=e84]: 8 KB
            - generic [ref=e85]: 演示文件
          - listitem [ref=e86]:
            - button "跨团队协作项目的长期研究资料与待确认事项汇总.md" [ref=e92] [cursor=pointer]
            - generic [ref=e93]: 10月9日 09:15
            - generic [ref=e94]: 32 KB
            - generic [ref=e95]: 演示文件
  - alert [ref=e96]
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