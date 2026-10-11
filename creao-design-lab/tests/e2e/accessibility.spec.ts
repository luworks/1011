import AxeBuilder from '@axe-core/playwright';
import { test, expect, type Page, type TestInfo } from '@playwright/test';

// An automated WCAG scan complements the existing explicit name, focus,
// interaction and geometry contracts; zero violations is not a full WCAG audit.
async function scan(page: Page, testInfo: TestInfo, state: string) {
  await page.evaluate(() => document.fonts.ready);
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();
  // Retain passes, inapplicable and incomplete as well as violations. Incomplete
  // findings require manual review; never silently turn them into passing rules.
  await testInfo.attach(`axe-${state}`, {
    body: JSON.stringify(results, null, 2),
    contentType: 'application/json',
  });
  testInfo.annotations.push({
    type: 'axe-incomplete',
    description: JSON.stringify(results.incomplete.map(({ id, nodes }) => ({ id, targets: nodes.map(node => node.target) }))),
  });
  expect(results.violations, `Automated WCAG A/AA violations in ${state}`).toEqual([]);
}

for (const viewport of [{ width: 1280, height: 900 }, { width: 390, height: 844 }]) {
  test.describe(`axe ${viewport.width}px`, () => {
    test.use({ viewport });

    test.beforeEach(async ({ browser }, testInfo) => {
      testInfo.annotations.push({ type: 'browser-version', description: browser.version() });
      testInfo.annotations.push({ type: 'browser-channel', description: process.env.PW_CHANNEL || 'bundled-chromium' });
    });

    test('[A11Y-002] axe Files initial', async ({ page }, testInfo) => {
      await page.goto('/files');
      await expect(page.getByTestId('file-item').first()).toBeVisible();
      await scan(page, testInfo, 'files-initial');
    });

    test('[A11Y-002] axe Files empty search', async ({ page }, testInfo) => {
      await page.goto('/files');
      await page.getByRole('searchbox', { name: '搜索文件和文件夹' }).fill('no-match-accessibility-4827');
      await expect(page.getByRole('heading', { name: '没有找到文件', exact: true })).toBeVisible();
      await expect(page.getByTestId('file-item')).toHaveCount(0);
      await scan(page, testInfo, 'files-empty-search');
    });

    test('[A11Y-002] axe Files folder validation error', async ({ page }, testInfo) => {
      await page.goto('/files');
      await page.getByRole('button', { name: '新建文件夹', exact: true }).click();
      await page.getByRole('button', { name: '创建文件夹', exact: true }).click();
      await expect(page.getByRole('main').getByRole('alert')).toHaveText('请输入文件夹名称。');
      await expect(page.getByRole('textbox', { name: '文件夹名称', exact: true })).toHaveAttribute('aria-invalid', 'true');
      await scan(page, testInfo, 'files-folder-error');
    });

    test('[A11Y-002] axe Files preview dialog', async ({ page }, testInfo) => {
      await page.goto('/files');
      const trigger = page.getByRole('button', { name: '季度研究摘要.md', exact: true });
      await trigger.click();
      const dialog = page.getByRole('dialog', { name: '季度研究摘要.md', exact: true });
      await expect(dialog).toBeVisible();
      await scan(page, testInfo, 'files-preview');
      await dialog.getByRole('button', { name: '关闭预览', exact: true }).click();
      await expect(dialog).not.toBeVisible();
      await expect(trigger).toBeFocused();
    });

    test('[A11Y-002] axe Connectors connected empty', async ({ page }, testInfo) => {
      await page.goto('/connectors');
      await page.getByRole('tab', { name: '已连接 (0)', exact: true }).click();
      await expect(page.getByRole('heading', { name: '暂无已连接的连接器', exact: true })).toBeVisible();
      await scan(page, testInfo, 'connectors-connected-empty');
    });

    test('[A11Y-002] axe Agents empty', async ({ page }, testInfo) => {
      await page.goto('/agents');
      await expect(page.getByRole('button', { name: '创建示例智能体', exact: true })).toBeVisible();
      await scan(page, testInfo, 'agents-empty');
    });

    test('[A11Y-002] axe Agents detail', async ({ page }, testInfo) => {
      await page.goto('/agents');
      await page.getByRole('button', { name: '创建示例智能体', exact: true }).click();
      await page.getByRole('button', { name: '查看详情', exact: true }).click();
      await expect(page.getByRole('heading', { level: 1, name: '研究助手', exact: true })).toBeVisible();
      await scan(page, testInfo, 'agents-detail');
    });

    test('[A11Y-002] axe Guidelines', async ({ page }, testInfo) => {
      await page.goto('/guidelines');
      await expect(page.getByRole('heading', { level: 1, name: '设计规范', exact: true })).toBeVisible();
      await scan(page, testInfo, 'guidelines');
    });
  });
}
