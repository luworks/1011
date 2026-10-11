# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: design.spec.ts >> [LAY-001] /connectors one visible page heading at 1280px
- Location: tests/e2e/design.spec.ts:18:9

# Error details

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  getByRole('main').getByRole('heading', { level: 1 })
Expected: 1
Received: 0
Timeout:  5000ms

Call log:
  - Expect "toHaveCount" getByRole('main').getByRole('heading', { level: 1 }) with timeout 5000ms
  - waiting for getByRole('main').getByRole('heading', { level: 1 })
    14 × locator resolved to 0 elements
       - unexpected value "0"

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
      - generic [ref=e28]:
        - heading "连接器" [level=2] [ref=e29]
        - paragraph [ref=e30]: 将日常工具带入你的工作流程。
      - paragraph [ref=e31]: 精选连接器
      - generic [ref=e32]:
        - article [ref=e33]:
          - generic [ref=e34]: S
          - generic [ref=e35]:
            - heading "Slack" [level=2] [ref=e36]
            - paragraph [ref=e37]: 在团队频道中分享进展、整理讨论。
        - article [ref=e38]:
          - generic [ref=e39]: D
          - generic [ref=e40]:
            - heading "Google Drive" [level=2] [ref=e41]
            - paragraph [ref=e42]: 查找项目文档，让资料触手可及。
      - generic [ref=e43]:
        - searchbox "搜索连接器" [ref=e48]
        - tablist "连接器状态" [ref=e49]:
          - tab "全部" [selected] [ref=e50] [cursor=pointer]
          - tab "可连接" [ref=e51] [cursor=pointer]
          - tab "已连接 (0)" [ref=e52] [cursor=pointer]
      - generic [ref=e53]:
        - generic [ref=e54]: 3 个结果
        - generic [ref=e55]: 仅本地演示，不会访问第三方账号。
      - tabpanel "全部" [ref=e56]:
        - generic [ref=e57]:
          - article [ref=e58]:
            - generic [ref=e59]: S
            - heading "Slack" [level=2] [ref=e60]
            - paragraph [ref=e61]: 在团队频道中分享进展、整理讨论。
            - button "模拟连接 Slack" [ref=e62] [cursor=pointer]: 模拟连接
          - article [ref=e64]:
            - generic [ref=e65]: D
            - heading "Google Drive" [level=2] [ref=e66]
            - paragraph [ref=e67]: 查找项目文档，让资料触手可及。
            - button "模拟连接 Google Drive" [ref=e68] [cursor=pointer]: 模拟连接
          - article [ref=e70]:
            - generic [ref=e71]: "N"
            - heading "Notion" [level=2] [ref=e72]
            - paragraph [ref=e73]: 整理知识库与项目笔记。
            - button "模拟连接 Notion" [ref=e74] [cursor=pointer]: 模拟连接
  - alert [ref=e76]
```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | import { knownFileContract } from './fixtures/file-contract';
  3   | 
  4   | test.beforeEach(async ({ browser }, testInfo) => {
  5   |   testInfo.annotations.push({ type: 'browser-version', description: browser.version() });
  6   |   testInfo.annotations.push({ type: 'browser-channel', description: process.env.PW_CHANNEL || 'bundled-chromium' });
  7   | });
  8   | 
  9   | const routes = [
  10  |   { path: '/files', heading: '文件' },
  11  |   { path: '/connectors', heading: '连接器' },
  12  |   { path: '/agents', heading: '智能体' },
  13  |   { path: '/guidelines', heading: '设计规范' },
  14  | ];
  15  | 
  16  | for (const width of [1280, 390]) {
  17  |   for (const route of routes) {
  18  |     test(`[LAY-001] ${route.path} one visible page heading at ${width}px`, async ({ page }) => {
  19  |       await page.setViewportSize({ width, height: 900 });
  20  |       await page.goto(route.path);
  21  |       const main = page.getByRole('main');
  22  |       await expect(main).toHaveCount(1);
  23  |       const headings = main.getByRole('heading', { level: 1 });
> 24  |       await expect(headings).toHaveCount(1);
      |                              ^ Error: expect(locator).toHaveCount(expected) failed
  25  |       await expect(headings).toBeVisible();
  26  |       await expect(headings).toHaveText(route.heading);
  27  |     });
  28  | 
  29  |     test(`[A11Y-001] ${route.path} visible controls retain accessible names at ${width}px`, async ({ page }) => {
  30  |       await page.setViewportSize({ width, height: 900 });
  31  |       await page.goto(route.path);
  32  |       await expect(page.getByRole('main')).toBeVisible();
  33  |       // Compute accessible names using Playwright's ARIA engine rather than reading a self-reported label flag.
  34  |       const controls = page.locator('button, input:not([type=hidden]), select, textarea, a[href], [role=button], [role=tab]');
  35  |       expect(await controls.count()).toBeGreaterThan(0);
  36  |       for (const control of await controls.all()) {
  37  |         if (await control.isVisible()) await expect(control).toHaveAccessibleName(/\S/);
  38  |       }
  39  |     });
  40  |   }
  41  | }
  42  | 
  43  | test('[STATE-001] connector empty state action reaches available services', async ({ page }) => {
  44  |   await page.goto('/connectors');
  45  |   await page.getByRole('tab', { name: /^已连接(?: \(\d+\))?$/ }).click();
  46  |   const recovery = page.getByRole('button', { name: '浏览可连接服务', exact: true });
  47  |   await expect(recovery).toBeVisible();
  48  |   await recovery.click();
  49  |   await expect(page.getByRole('tab', { name: '可连接', exact: true })).toHaveAttribute('aria-selected', 'true');
  50  |   await expect(page.getByRole('button', { name: /连接/ }).first()).toBeVisible();
  51  |   await expect(recovery).toHaveCount(0);
  52  | });
  53  | 
  54  | test('[NAV-001] empty-state destination copy matches actual available tab', async ({ page }) => {
  55  |   await page.goto('/connectors');
  56  |   const destination = page.getByRole('tab', { name: '可连接', exact: true });
  57  |   await expect(destination).toBeVisible();
  58  |   await page.getByRole('tab', { name: /^已连接(?: \(\d+\))?$/ }).click();
  59  |   // The guidance must name the destination itself, not an obsolete synonym.
  60  |   await expect(page.getByRole('main')).toContainText('可连接');
  61  |   const guidance = page.getByTestId('empty-state-description');
  62  |   await expect(guidance).toContainText('可连接');
  63  |   await expect(guidance).not.toContainText('可用');
  64  |   await page.getByRole('button', { name: '浏览可连接服务', exact: true }).click();
  65  |   await expect(destination).toHaveAttribute('aria-selected', 'true');
  66  | });
  67  | 
  68  | test('[STATE-001] file search no-results action restores actual entries', async ({ page }) => {
  69  |   await page.goto('/files');
  70  |   const search = page.getByRole('searchbox', { name: '搜索文件和文件夹' });
  71  |   await search.fill('no-file-matches-928371');
  72  |   await expect(page.getByTestId('file-item')).toHaveCount(0);
  73  |   await page.getByTestId('empty-state-description').locator('..').getByRole('button', { name: '清除搜索', exact: true }).click();
  74  |   await expect(search).toHaveValue('');
  75  |   await expect(page.getByTestId('file-item').first()).toBeVisible();
  76  | });
  77  | 
  78  | test('[RESP-001] file list preserves field labels and fits 390px viewport', async ({ page }, testInfo) => {
  79  |   await page.setViewportSize({ width: 390, height: 900 });
  80  |   await page.goto('/files');
  81  |   await page.getByRole('button', { name: '列表视图', exact: true }).click();
  82  |   await expect(page.getByTestId('desktop-file-header')).toBeHidden();
  83  |   const items = page.getByTestId('file-item');
  84  |   expect(await items.count()).toBeGreaterThan(0);
  85  |   const knownItem=items.filter({ has: page.getByRole('button', { name: knownFileContract.name, exact: true }) });
  86  |   await expect(knownItem).toHaveCount(1);
  87  |   for (const field of knownFileContract.fields) {
  88  |     const label=knownItem.getByTestId('file-meta-label').filter({ hasText: new RegExp(`^${field.label}$`) });
  89  |     await expect(label).toHaveCount(1);
  90  |     await expect(label.locator('..')).toHaveText(`${field.label}${field.value}`);
  91  |   }
  92  |   for (const item of await items.all()) {
  93  |     await expect(item).toBeVisible();
  94  |     const labels=item.getByTestId('file-meta-label');
  95  |     await expect(labels).toHaveText(knownFileContract.fields.map(field => field.label));
  96  |     for(const label of await labels.all()) await expect(label).toBeVisible();
  97  |     const box=await item.boundingBox();
  98  |     expect(box).not.toBeNull();
  99  |     expect(box!.x).toBeGreaterThanOrEqual(0);
  100 |     expect(box!.x+box!.width).toBeLessThanOrEqual(391);
  101 |     const geometry=await item.evaluate(element=>{
  102 |       const fields=[...element.querySelectorAll('[data-testid="file-meta-label"]')].map(label=>label.parentElement!.getBoundingClientRect());
  103 |       return fields.map(field=>({left:field.left,right:field.right,top:field.top,bottom:field.bottom}));
  104 |     });
  105 |     for(let a=0;a<geometry.length;a++)for(let b=a+1;b<geometry.length;b++){
  106 |       const x=Math.min(geometry[a].right,geometry[b].right)-Math.max(geometry[a].left,geometry[b].left);
  107 |       const y=Math.min(geometry[a].bottom,geometry[b].bottom)-Math.max(geometry[a].top,geometry[b].top);
  108 |       expect(x>1&&y>1,'File metadata fields overlap').toBe(false);
  109 |     }
  110 |   }
  111 |   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
  112 |   expect(overflow,'Document has horizontal clipping/overflow').toBe(false);
  113 |   await testInfo.attach('files-390px', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
  114 |   await page.setViewportSize({ width: 1280, height: 900 });
  115 |   await expect(page.getByTestId('desktop-file-header')).toBeVisible();
  116 |   for(const label of await page.getByTestId('file-meta-label').all())await expect(label).toBeHidden();
  117 |   await testInfo.attach('files-1280px', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
  118 | });
  119 | 
  120 | for(const width of [320,800]) {
  121 |   test(`[RESP-001] file list has no horizontal overflow at ${width}px`, async ({ page }, testInfo) => {
  122 |     await page.setViewportSize({ width, height: 900 });
  123 |     await page.goto('/files');
  124 |     await expect(page.getByRole('heading', { level: 1, name: '文件', exact: true })).toBeVisible();
```