import { readReference } from '@/lib/read-reference';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { PageHeader } from '@/components/patterns/PageHeader';
import { referenceFiles, referenceHref } from '@/lib/references';
export const dynamic = 'force-dynamic';
export default async function ReferencePage({ searchParams }: { searchParams: Promise<{ file?: string; group?: string }> }) {
  const { file, group } = await searchParams;
  const selected = referenceFiles.find(allowed => allowed === file);
  const files = group ? referenceFiles.filter(allowed => allowed.startsWith(group) && group.endsWith('/')) : [];
  if (!selected && files.length === 0) notFound();
  const content = selected ? await readReference(selected).catch(() => null) : null;
  if (selected && content === null) notFound();
  return <><PageHeader title={selected ?? '规范源码索引'} description="当前本地文件的只读内容。" actions={<Link className="button" href="/guidelines">返回设计规范</Link>} />{selected ? <pre className="source-view"><code>{content}</code></pre> : <ul className="reference-list">{files.map(item => <li key={item}><Link href={referenceHref(item)!}>{item}</Link></li>)}</ul>}</>;
}
