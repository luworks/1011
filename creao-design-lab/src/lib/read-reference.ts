import { readFile } from 'node:fs/promises';
import path from 'node:path';
import type { referenceFiles } from './references';

// Literal paths preserve Next's precise file tracing; only this allowlist is exposed.
export function readReference(file: typeof referenceFiles[number]) {
  switch (file) {
    case 'design.md': return readFile(path.join(process.cwd(), 'design.md'), 'utf8');
    case 'AGENTS.md': return readFile(path.join(process.cwd(), 'AGENTS.md'), 'utf8');
    case 'package.json': return readFile(path.join(process.cwd(), 'package.json'), 'utf8');
    case 'src/styles/tokens.css': return readFile(path.join(process.cwd(), 'src/styles/tokens.css'), 'utf8');
    case 'src/styles/components.css': return readFile(path.join(process.cwd(), 'src/styles/components.css'), 'utf8');
    case 'src/styles/layouts.css': return readFile(path.join(process.cwd(), 'src/styles/layouts.css'), 'utf8');
    case 'src/components/ui/index.tsx': return readFile(path.join(process.cwd(), 'src/components/ui/index.tsx'), 'utf8');
    case 'src/components/patterns/PageHeader.tsx': return readFile(path.join(process.cwd(), 'src/components/patterns/PageHeader.tsx'), 'utf8');
    case 'src/components/patterns/EmptyState.tsx': return readFile(path.join(process.cwd(), 'src/components/patterns/EmptyState.tsx'), 'utf8');
    case 'src/components/patterns/Shell.tsx': return readFile(path.join(process.cwd(), 'src/components/patterns/Shell.tsx'), 'utf8');
    case 'src/lib/copy.ts': return readFile(path.join(process.cwd(), 'src/lib/copy.ts'), 'utf8');
    case 'src/lib/data.ts': return readFile(path.join(process.cwd(), 'src/lib/data.ts'), 'utf8');
    case 'governance/rules.json': return readFile(path.join(process.cwd(), 'governance/rules.json'), 'utf8');
    case 'governance/exceptions.json': return readFile(path.join(process.cwd(), 'governance/exceptions.json'), 'utf8');
    case 'scripts/check-design.mjs': return readFile(path.join(process.cwd(), 'scripts/check-design.mjs'), 'utf8');
    case 'scripts/mutation-runner.mjs': return readFile(path.join(process.cwd(), 'scripts/mutation-runner.mjs'), 'utf8');
    case 'tests/e2e/design.spec.ts': return readFile(path.join(process.cwd(), 'tests/e2e/design.spec.ts'), 'utf8');
    case 'tests/mutations/cases.mjs': return readFile(path.join(process.cwd(), 'tests/mutations/cases.mjs'), 'utf8');
  }
}
