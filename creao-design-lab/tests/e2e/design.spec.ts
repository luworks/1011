import { test, expect } from '@playwright/test';
import { knownFileContract } from './fixtures/file-contract';

test.beforeEach(async ({ browser }, testInfo) => {
  testInfo.annotations.push({ type: 'browser-version', description: browser.version() });
  testInfo.annotations.push({ type: 'browser-channel', description: process.env.PW_CHANNEL || 'bundled-chromium' });
});

const routes = [
  { path: '/files', heading: '文件' },
  { path: '/connectors', heading: '连接器' },
  { path: '/agents', heading: '智能体' },
  { path: '/guidelines', heading: '设计规范' },
];

for (const width of [1280, 390]) {
  for (const route of routes) {
    test(`[LAY-001] ${route.path} one visible page heading at ${width}px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      await page.goto(route.path);
      const main = page.getByRole('main');
      await expect(main).toHaveCount(1);
      const headings = main.getByRole('heading', { level: 1 });
      await expect(headings).toHaveCount(1);
      await expect(headings).toBeVisible();
      await expect(headings).toHaveText(route.heading);
    });

    test(`[A11Y-001] ${route.path} visible controls retain accessible names at ${width}px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      await page.goto(route.path);
      await expect(page.getByRole('main')).toBeVisible();
      // Compute accessible names using Playwright's ARIA engine rather than reading a self-reported label flag.
      const controls = page.locator('button, input:not([type=hidden]), select, textarea, a[href], [role=button], [role=tab]');
      expect(await controls.count()).toBeGreaterThan(0);
      for (const control of await controls.all()) {
        if (await control.isVisible()) await expect(control).toHaveAccessibleName(/\S/);
      }
    });
  }
}

test('[STATE-001] connector empty state action reaches available services', async ({ page }) => {
  await page.goto('/connectors');
  await page.getByRole('tab', { name: /^已连接(?: \(\d+\))?$/ }).click();
  const recovery = page.getByRole('button', { name: '浏览可连接服务', exact: true });
  await expect(recovery).toBeVisible();
  await recovery.click();
  await expect(page.getByRole('tab', { name: '可连接', exact: true })).toHaveAttribute('aria-selected', 'true');
  await expect(page.getByRole('button', { name: /连接/ }).first()).toBeVisible();
  await expect(recovery).toHaveCount(0);
});

test('[NAV-001] empty-state destination copy matches actual available tab', async ({ page }) => {
  await page.goto('/connectors');
  const destination = page.getByRole('tab', { name: '可连接', exact: true });
  await expect(destination).toBeVisible();
  await page.getByRole('tab', { name: /^已连接(?: \(\d+\))?$/ }).click();
  // The guidance must name the destination itself, not an obsolete synonym.
  await expect(page.getByRole('main')).toContainText('可连接');
  const guidance = page.getByTestId('empty-state-description');
  await expect(guidance).toContainText('可连接');
  await expect(guidance).not.toContainText('可用');
  await page.getByRole('button', { name: '浏览可连接服务', exact: true }).click();
  await expect(destination).toHaveAttribute('aria-selected', 'true');
});

test('[STATE-001] file search no-results action restores actual entries', async ({ page }) => {
  await page.goto('/files');
  const search = page.getByRole('searchbox', { name: '搜索文件和文件夹' });
  await search.fill('no-file-matches-928371');
  await expect(page.getByTestId('file-item')).toHaveCount(0);
  await page.getByTestId('empty-state-description').locator('..').getByRole('button', { name: '清除搜索', exact: true }).click();
  await expect(search).toHaveValue('');
  await expect(page.getByTestId('file-item').first()).toBeVisible();
});

test('[RESP-001] file list preserves field labels and fits 390px viewport', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 900 });
  await page.goto('/files');
  await page.getByRole('button', { name: '列表视图', exact: true }).click();
  await expect(page.getByTestId('desktop-file-header')).toBeHidden();
  const items = page.getByTestId('file-item');
  expect(await items.count()).toBeGreaterThan(0);
  const knownItem=items.filter({ has: page.getByRole('button', { name: knownFileContract.name, exact: true }) });
  await expect(knownItem).toHaveCount(1);
  for (const field of knownFileContract.fields) {
    const label=knownItem.getByTestId('file-meta-label').filter({ hasText: new RegExp(`^${field.label}$`) });
    await expect(label).toHaveCount(1);
    await expect(label.locator('..')).toHaveText(`${field.label}${field.value}`);
  }
  for (const item of await items.all()) {
    await expect(item).toBeVisible();
    const labels=item.getByTestId('file-meta-label');
    await expect(labels).toHaveText(knownFileContract.fields.map(field => field.label));
    for(const label of await labels.all()) await expect(label).toBeVisible();
    const box=await item.boundingBox();
    expect(box).not.toBeNull();
    expect(box!.x).toBeGreaterThanOrEqual(0);
    expect(box!.x+box!.width).toBeLessThanOrEqual(391);
    const geometry=await item.evaluate(element=>{
      const fields=[...element.querySelectorAll('[data-testid="file-meta-label"]')].map(label=>label.parentElement!.getBoundingClientRect());
      return fields.map(field=>({left:field.left,right:field.right,top:field.top,bottom:field.bottom}));
    });
    for(let a=0;a<geometry.length;a++)for(let b=a+1;b<geometry.length;b++){
      const x=Math.min(geometry[a].right,geometry[b].right)-Math.max(geometry[a].left,geometry[b].left);
      const y=Math.min(geometry[a].bottom,geometry[b].bottom)-Math.max(geometry[a].top,geometry[b].top);
      expect(x>1&&y>1,'File metadata fields overlap').toBe(false);
    }
  }
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
  expect(overflow,'Document has horizontal clipping/overflow').toBe(false);
  await testInfo.attach('files-390px', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
  await page.setViewportSize({ width: 1280, height: 900 });
  await expect(page.getByTestId('desktop-file-header')).toBeVisible();
  for(const label of await page.getByTestId('file-meta-label').all())await expect(label).toBeHidden();
  await testInfo.attach('files-1280px', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
});

for(const width of [320,800]) {
  test(`[RESP-001] file list has no horizontal overflow at ${width}px`, async ({ page }, testInfo) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/files');
    await expect(page.getByRole('heading', { level: 1, name: '文件', exact: true })).toBeVisible();
    await page.getByRole('button', { name: '列表视图', exact: true }).click();
    await expect(page.getByTestId('desktop-file-header')).toBeHidden();
    for(const label of await page.getByTestId('file-meta-label').all()) await expect(label).toBeVisible();
    const dimensions=await page.evaluate(()=>({document:document.documentElement.scrollWidth,viewport:window.innerWidth}));
    expect(dimensions.document,'File list must fit intermediate and compact viewport widths').toBeLessThanOrEqual(dimensions.viewport+1);
    for(const item of await page.getByTestId('file-item').all()) {
      const box=await item.boundingBox();
      expect(box).not.toBeNull();
      expect(box!.x).toBeGreaterThanOrEqual(0);
      expect(box!.x+box!.width).toBeLessThanOrEqual(width+1);
    }
    await testInfo.attach(`files-${width}px`, { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
  });
}
