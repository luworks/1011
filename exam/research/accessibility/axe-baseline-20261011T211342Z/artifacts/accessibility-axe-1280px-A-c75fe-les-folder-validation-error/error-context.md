# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: accessibility.spec.ts >> axe 1280px >> [A11Y-001] axe Files folder validation error
- Location: tests/e2e/accessibility.spec.ts:47:9

# Error details

```
Error: expect(locator).toHaveText(expected) failed

Locator: getByRole('alert')
Expected: "请输入文件夹名称。"
Error: strict mode violation: getByRole('alert') resolved to 2 elements:
    1) <p role="alert" class="error" id="folder-error">请输入文件夹名称。</p> aka getByText('请输入文件夹名称。')
    2) <div role="alert" aria-live="assertive" id="__next-route-announcer__"></div> aka locator('[id="__next-route-announcer__"]')

Call log:
  - Expect "toHaveText" getByRole('alert') with timeout 5000ms
  - waiting for getByRole('alert')

```

# Page snapshot

```yaml
- generic [ref=e1]:
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
        - generic "文件显示方式" [ref=e41]:
          - button "列表视图" [pressed] [ref=e42] [cursor=pointer]
          - button "网格视图" [ref=e44] [cursor=pointer]
      - generic [ref=e47]:
        - generic [ref=e48]: 文件夹名称
        - textbox "文件夹名称" [invalid] [ref=e49]
        - button "创建文件夹" [active] [ref=e50] [cursor=pointer]
        - button "取消" [ref=e51] [cursor=pointer]
        - alert [ref=e52]: 请输入文件夹名称。
      - status [ref=e53]
      - generic [ref=e54]:
        - generic [aria-hidden] [ref=e55]:
          - generic [ref=e56]: 名称
          - generic [ref=e57]: 修改时间
          - generic [ref=e58]: 大小
          - generic [ref=e59]: 来源
        - list [ref=e60]:
          - listitem [ref=e61]:
            - button "季度研究摘要.md" [ref=e67] [cursor=pointer]
            - generic [ref=e68]: 10月11日 10:30
            - generic [ref=e69]: 12 KB
            - generic [ref=e70]: 演示文件
          - listitem [ref=e71]:
            - button "产品需求与设计评审记录.md" [ref=e77] [cursor=pointer]
            - generic [ref=e78]: 10月10日 16:45
            - generic [ref=e79]: 24 KB
            - generic [ref=e80]: 演示文件
          - listitem [ref=e81]:
            - button "团队工作空间布局草图.svg" [ref=e88] [cursor=pointer]
            - generic [ref=e89]: 10月10日 11:20
            - generic [ref=e90]: 8 KB
            - generic [ref=e91]: 演示文件
          - listitem [ref=e92]:
            - button "跨团队协作项目的长期研究资料与待确认事项汇总.md" [ref=e98] [cursor=pointer]
            - generic [ref=e99]: 10月9日 09:15
            - generic [ref=e100]: 32 KB
            - generic [ref=e101]: 演示文件
  - alert [ref=e102]
```

# Test source

```ts
  1  | import AxeBuilder from '@axe-core/playwright';
  2  | import { test, expect, type Page, type TestInfo } from '@playwright/test';
  3  | 
  4  | // An automated WCAG scan complements the existing explicit name, focus,
  5  | // interaction and geometry contracts; zero violations is not a full WCAG audit.
  6  | async function scan(page: Page, testInfo: TestInfo, state: string) {
  7  |   await page.evaluate(() => document.fonts.ready);
  8  |   const results = await new AxeBuilder({ page })
  9  |     .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
  10 |     .analyze();
  11 |   // Retain passes, inapplicable and incomplete as well as violations. Incomplete
  12 |   // findings require manual review; never silently turn them into passing rules.
  13 |   await testInfo.attach(`axe-${state}`, {
  14 |     body: JSON.stringify(results, null, 2),
  15 |     contentType: 'application/json',
  16 |   });
  17 |   testInfo.annotations.push({
  18 |     type: 'axe-incomplete',
  19 |     description: JSON.stringify(results.incomplete.map(({ id, nodes }) => ({ id, targets: nodes.map(node => node.target) }))),
  20 |   });
  21 |   expect(results.violations, `Automated WCAG A/AA violations in ${state}`).toEqual([]);
  22 | }
  23 | 
  24 | for (const viewport of [{ width: 1280, height: 900 }, { width: 390, height: 844 }]) {
  25 |   test.describe(`axe ${viewport.width}px`, () => {
  26 |     test.use({ viewport });
  27 | 
  28 |     test.beforeEach(async ({ browser }, testInfo) => {
  29 |       testInfo.annotations.push({ type: 'browser-version', description: browser.version() });
  30 |       testInfo.annotations.push({ type: 'browser-channel', description: process.env.PW_CHANNEL || 'bundled-chromium' });
  31 |     });
  32 | 
  33 |     test('[A11Y-001] axe Files initial', async ({ page }, testInfo) => {
  34 |       await page.goto('/files');
  35 |       await expect(page.getByTestId('file-item').first()).toBeVisible();
  36 |       await scan(page, testInfo, 'files-initial');
  37 |     });
  38 | 
  39 |     test('[A11Y-001] axe Files empty search', async ({ page }, testInfo) => {
  40 |       await page.goto('/files');
  41 |       await page.getByRole('searchbox', { name: '搜索文件和文件夹' }).fill('no-match-accessibility-4827');
  42 |       await expect(page.getByRole('heading', { name: '没有找到文件', exact: true })).toBeVisible();
  43 |       await expect(page.getByTestId('file-item')).toHaveCount(0);
  44 |       await scan(page, testInfo, 'files-empty-search');
  45 |     });
  46 | 
  47 |     test('[A11Y-001] axe Files folder validation error', async ({ page }, testInfo) => {
  48 |       await page.goto('/files');
  49 |       await page.getByRole('button', { name: '新建文件夹', exact: true }).click();
  50 |       await page.getByRole('button', { name: '创建文件夹', exact: true }).click();
> 51 |       await expect(page.getByRole('alert')).toHaveText('请输入文件夹名称。');
     |                                             ^ Error: expect(locator).toHaveText(expected) failed
  52 |       await expect(page.getByRole('textbox', { name: '文件夹名称', exact: true })).toHaveAttribute('aria-invalid', 'true');
  53 |       await scan(page, testInfo, 'files-folder-error');
  54 |     });
  55 | 
  56 |     test('[A11Y-001] axe Files preview dialog', async ({ page }, testInfo) => {
  57 |       await page.goto('/files');
  58 |       const trigger = page.getByRole('button', { name: '季度研究摘要.md', exact: true });
  59 |       await trigger.click();
  60 |       const dialog = page.getByRole('dialog', { name: '季度研究摘要.md', exact: true });
  61 |       await expect(dialog).toBeVisible();
  62 |       await scan(page, testInfo, 'files-preview');
  63 |       await dialog.getByRole('button', { name: '关闭预览', exact: true }).click();
  64 |       await expect(dialog).not.toBeVisible();
  65 |       await expect(trigger).toBeFocused();
  66 |     });
  67 | 
  68 |     test('[A11Y-001] axe Connectors connected empty', async ({ page }, testInfo) => {
  69 |       await page.goto('/connectors');
  70 |       await page.getByRole('tab', { name: '已连接 (0)', exact: true }).click();
  71 |       await expect(page.getByRole('heading', { name: '暂无已连接的连接器', exact: true })).toBeVisible();
  72 |       await scan(page, testInfo, 'connectors-connected-empty');
  73 |     });
  74 | 
  75 |     test('[A11Y-001] axe Agents empty', async ({ page }, testInfo) => {
  76 |       await page.goto('/agents');
  77 |       await expect(page.getByRole('button', { name: '创建示例智能体', exact: true })).toBeVisible();
  78 |       await scan(page, testInfo, 'agents-empty');
  79 |     });
  80 | 
  81 |     test('[A11Y-001] axe Agents detail', async ({ page }, testInfo) => {
  82 |       await page.goto('/agents');
  83 |       await page.getByRole('button', { name: '创建示例智能体', exact: true }).click();
  84 |       await page.getByRole('button', { name: '查看详情', exact: true }).click();
  85 |       await expect(page.getByRole('heading', { level: 1, name: '研究助手', exact: true })).toBeVisible();
  86 |       await scan(page, testInfo, 'agents-detail');
  87 |     });
  88 | 
  89 |     test('[A11Y-001] axe Guidelines', async ({ page }, testInfo) => {
  90 |       await page.goto('/guidelines');
  91 |       await expect(page.getByRole('heading', { level: 1, name: '设计规范', exact: true })).toBeVisible();
  92 |       await scan(page, testInfo, 'guidelines');
  93 |     });
  94 |   });
  95 | }
  96 | 
```