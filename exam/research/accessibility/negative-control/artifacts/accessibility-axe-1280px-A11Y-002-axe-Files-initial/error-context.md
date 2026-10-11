# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: accessibility.spec.ts >> axe 1280px >> [A11Y-002] axe Files initial
- Location: tests/e2e/accessibility.spec.ts:33:9

# Error details

```
Error: Automated WCAG A/AA violations in files-initial

expect(received).toEqual(expected) // deep equality

- Expected  -  1
+ Received  + 42

- Array []
+ Array [
+   Object {
+     "description": "Ensure all ARIA attributes have valid values",
+     "help": "ARIA attributes must conform to valid values",
+     "helpUrl": "https://dequeuniversity.com/rules/axe/4.13/aria-valid-attr-value?application=playwright",
+     "id": "aria-valid-attr-value",
+     "impact": "critical",
+     "nodes": Array [
+       Object {
+         "all": Array [
+           Object {
+             "data": Array [
+               "aria-pressed=\"sometimes\"",
+             ],
+             "id": "aria-valid-attr-value",
+             "impact": "critical",
+             "message": "Invalid ARIA attribute value: aria-pressed=\"sometimes\"",
+             "relatedNodes": Array [],
+           },
+         ],
+         "any": Array [],
+         "failureSummary": "Fix all of the following:
+   Invalid ARIA attribute value: aria-pressed=\"sometimes\"",
+         "html": "<button type=\"button\" class=\"button button-ghost \" aria-label=\"列表视图\" aria-pressed=\"sometimes\">",
+         "impact": "critical",
+         "none": Array [],
+         "target": Array [
+           "button[aria-label=\"列表视图\"]",
+         ],
+       },
+     ],
+     "tags": Array [
+       "cat.aria",
+       "wcag2a",
+       "wcag412",
+       "EN-301-549",
+       "EN-9.4.1.2",
+       "RGAAv4",
+       "RGAA-7.1.1",
+     ],
+   },
+ ]
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
        - generic "文件显示方式" [ref=e41]:
          - button "列表视图" [ref=e42] [cursor=pointer]
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
> 21 |   expect(results.violations, `Automated WCAG A/AA violations in ${state}`).toEqual([]);
     |                                                                            ^ Error: Automated WCAG A/AA violations in files-initial
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
  33 |     test('[A11Y-002] axe Files initial', async ({ page }, testInfo) => {
  34 |       await page.goto('/files');
  35 |       await expect(page.getByTestId('file-item').first()).toBeVisible();
  36 |       await scan(page, testInfo, 'files-initial');
  37 |     });
  38 | 
  39 |     test('[A11Y-002] axe Files empty search', async ({ page }, testInfo) => {
  40 |       await page.goto('/files');
  41 |       await page.getByRole('searchbox', { name: '搜索文件和文件夹' }).fill('no-match-accessibility-4827');
  42 |       await expect(page.getByRole('heading', { name: '没有找到文件', exact: true })).toBeVisible();
  43 |       await expect(page.getByTestId('file-item')).toHaveCount(0);
  44 |       await scan(page, testInfo, 'files-empty-search');
  45 |     });
  46 | 
  47 |     test('[A11Y-002] axe Files folder validation error', async ({ page }, testInfo) => {
  48 |       await page.goto('/files');
  49 |       await page.getByRole('button', { name: '新建文件夹', exact: true }).click();
  50 |       await page.getByRole('button', { name: '创建文件夹', exact: true }).click();
  51 |       await expect(page.getByRole('main').getByRole('alert')).toHaveText('请输入文件夹名称。');
  52 |       await expect(page.getByRole('textbox', { name: '文件夹名称', exact: true })).toHaveAttribute('aria-invalid', 'true');
  53 |       await scan(page, testInfo, 'files-folder-error');
  54 |     });
  55 | 
  56 |     test('[A11Y-002] axe Files preview dialog', async ({ page }, testInfo) => {
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
  68 |     test('[A11Y-002] axe Connectors connected empty', async ({ page }, testInfo) => {
  69 |       await page.goto('/connectors');
  70 |       await page.getByRole('tab', { name: '已连接 (0)', exact: true }).click();
  71 |       await expect(page.getByRole('heading', { name: '暂无已连接的连接器', exact: true })).toBeVisible();
  72 |       await scan(page, testInfo, 'connectors-connected-empty');
  73 |     });
  74 | 
  75 |     test('[A11Y-002] axe Agents empty', async ({ page }, testInfo) => {
  76 |       await page.goto('/agents');
  77 |       await expect(page.getByRole('button', { name: '创建示例智能体', exact: true })).toBeVisible();
  78 |       await scan(page, testInfo, 'agents-empty');
  79 |     });
  80 | 
  81 |     test('[A11Y-002] axe Agents detail', async ({ page }, testInfo) => {
  82 |       await page.goto('/agents');
  83 |       await page.getByRole('button', { name: '创建示例智能体', exact: true }).click();
  84 |       await page.getByRole('button', { name: '查看详情', exact: true }).click();
  85 |       await expect(page.getByRole('heading', { level: 1, name: '研究助手', exact: true })).toBeVisible();
  86 |       await scan(page, testInfo, 'agents-detail');
  87 |     });
  88 | 
  89 |     test('[A11Y-002] axe Guidelines', async ({ page }, testInfo) => {
  90 |       await page.goto('/guidelines');
  91 |       await expect(page.getByRole('heading', { level: 1, name: '设计规范', exact: true })).toBeVisible();
  92 |       await scan(page, testInfo, 'guidelines');
  93 |     });
  94 |   });
  95 | }
  96 | 
```