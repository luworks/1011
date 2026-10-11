// Explicit allowlist: request input never becomes a filesystem path.
export const referenceFiles = [
  'design.md', 'AGENTS.md', 'package.json',
  'src/styles/tokens.css', 'src/styles/components.css', 'src/styles/layouts.css',
  'src/components/ui/index.tsx',
  'src/components/patterns/PageHeader.tsx', 'src/components/patterns/EmptyState.tsx', 'src/components/patterns/Shell.tsx',
  'src/lib/copy.ts', 'src/lib/data.ts',
  'governance/rules.json', 'governance/exceptions.json',
  'scripts/check-design.mjs', 'scripts/mutation-runner.mjs',
  'tests/e2e/design.spec.ts', 'tests/mutations/cases.mjs',
] as const;
export function referenceHref(href: string): string | null {
  const clean = href.replace(/^\.\//, '');
  if (referenceFiles.some(file => file === clean)) return `/reference?file=${encodeURIComponent(clean)}`;
  if (clean.endsWith('/') && referenceFiles.some(file => file.startsWith(clean))) return `/reference?group=${encodeURIComponent(clean)}`;
  return null;
}
