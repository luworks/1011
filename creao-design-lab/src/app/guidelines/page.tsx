import { readFile } from 'node:fs/promises';
import path from 'node:path';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { PageHeader } from '@/components/patterns/PageHeader';
import { copy } from '@/lib/copy';
import { referenceHref } from '@/lib/references';
export const dynamic = 'force-dynamic';
export default async function GuidelinesPage() {
  const markdown = await readFile(path.join(process.cwd(), 'design.md'), 'utf8').catch(() => copy.guidelines.missing);
  return <><PageHeader title={copy.guidelines.title} description={copy.guidelines.description} /><article className="guideline-prose"><Markdown remarkPlugins={[remarkGfm]} components={{ pre: ({ children }) => <pre tabIndex={0}>{children}</pre>, table: ({ children }) => <table tabIndex={0}>{children}</table>, h1: ({ children }) => <h2>{children}</h2>, h2: ({ children }) => <h3>{children}</h3>, h3: ({ children }) => <h4>{children}</h4>, a: ({ href = '', children }) => { const local = referenceHref(href); if (local) return <a href={local}>{children}</a>; if (/^https:\/\//.test(href)) return <a href={href} rel="noreferrer">{children}</a>; if (href.startsWith('#')) return <a href={href}>{children}</a>; return <span>{children}<small className="offline-reference"> {copy.guidelines.attachment}</small></span>; } }}>{markdown}</Markdown></article></>;
}
