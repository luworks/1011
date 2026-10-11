# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: design.spec.ts >> [A11Y-001] /files visible controls retain accessible names at 1280px
- Location: tests/e2e/design.spec.ts:29:9

# Error details

```
Error: expect(locator).toHaveAccessibleName(expected) failed

Locator: locator('button, input:not([type=hidden]), select, textarea, a[href], [role=button], [role=tab]').nth(13)
Expected pattern: /\S/
Received string:  ""
Timeout: 5000ms

Call log:
  - Expect "toHaveAccessibleName" locator('button, input:not([type=hidden]), select, textarea, a[href], [role=button], [role=tab]').nth(13) with timeout 5000ms
  - waiting for locator('button, input:not([type=hidden]), select, textarea, a[href], [role=button], [role=tab]').nth(13)
    14 × locator resolved to <button type="button" aria-pressed="false" class="important-star" data-file-id="research" data-testid="important-toggle">…</button>
       - unexpected value ""

```

```yaml
- button
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
  24  |       await expect(headings).toHaveCount(1);
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
> 37  |         if (await control.isVisible()) await expect(control).toHaveAccessibleName(/\S/);
      |                                                              ^ Error: expect(locator).toHaveAccessibleName(expected) failed
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
  125 |     await page.getByRole('button', { name: '列表视图', exact: true }).click();
  126 |     await expect(page.getByTestId('desktop-file-header')).toBeHidden();
  127 |     for(const label of await page.getByTestId('file-meta-label').all()) await expect(label).toBeVisible();
  128 |     const dimensions=await page.evaluate(()=>({document:document.documentElement.scrollWidth,viewport:window.innerWidth}));
  129 |     expect(dimensions.document,'File list must fit intermediate and compact viewport widths').toBeLessThanOrEqual(dimensions.viewport+1);
  130 |     for(const item of await page.getByTestId('file-item').all()) {
  131 |       const box=await item.boundingBox();
  132 |       expect(box).not.toBeNull();
  133 |       expect(box!.x).toBeGreaterThanOrEqual(0);
  134 |       expect(box!.x+box!.width).toBeLessThanOrEqual(width+1);
  135 |     }
  136 |     await testInfo.attach(`files-${width}px`, { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
  137 |   });
```