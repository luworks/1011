'use client';
import { useState } from 'react';
import { Button, Icon } from '@/components/ui';
import { PageHeader } from '@/components/patterns/PageHeader';
import { EmptyState } from '@/components/patterns/EmptyState';
import { copy } from '@/lib/copy';
export default function AgentsPage() { const [created, setCreated] = useState(false); const [detail, setDetail] = useState(false); const [result, setResult] = useState(false);
  if (detail) return <><PageHeader title={copy.agents.detailTitle} description={copy.agents.demo} actions={<Button onClick={() => setDetail(false)}><Icon name="back" />{copy.agents.back}</Button>} /><section className="detail-card"><span className="badge">{copy.agents.status}</span><h2>{copy.agents.task}</h2><p>{copy.agents.body}</p><Button variant="primary" onClick={() => setResult(true)}>{copy.agents.run}</Button>{result && <section className="example-result" role="status"><h2>{copy.agents.resultTitle}</h2><p>{copy.agents.result}</p></section>}</section></>;
  return <><PageHeader title={copy.agents.title} />{!created ? <EmptyState icon="bot" title={copy.agents.emptyTitle} description={copy.agents.emptyDescription} action={{ label: copy.agents.create, onClick: () => setCreated(true) }} /> : <article className="agent-card"><span className="empty-icon"><Icon name="bot" /></span><div><h2>{copy.agents.name}</h2><p>{copy.agents.description}</p><span className="badge">{copy.agents.status}</span></div><Button onClick={() => setDetail(true)}>{copy.agents.details}<Icon name="chevron" /></Button></article>}<p className="footnote">{copy.agents.demo}</p></>;
}
