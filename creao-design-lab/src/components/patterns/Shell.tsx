'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, type ReactNode } from 'react';
import { Button, Icon } from '@/components/ui';
import { copy } from '@/lib/copy';
const links = [{ href: '/agents', label: copy.nav.agents, icon: 'bot' }, { href: '/files', label: copy.nav.files, icon: 'files' }, { href: '/connectors', label: copy.nav.connectors, icon: 'plug' }, { href: '/guidelines', label: copy.nav.guidelines, icon: 'book' }];
export function Shell({ children }: { children: ReactNode }) {
  const pathname = usePathname(); const [open, setOpen] = useState(false);
  return <div className="app-shell"><a className="skip-link" href="#main-content">{copy.skip}</a><div className="mobile-bar"><Button variant="ghost" aria-label={copy.menu} aria-expanded={open} aria-controls="primary-navigation" onClick={() => setOpen(!open)}><Icon name="menu" /></Button><span className="wordmark">{copy.brand}</span></div><aside className={`sidebar ${open ? 'sidebar-open' : ''}`}><Link href="/files" className="wordmark" onClick={() => setOpen(false)}>{copy.brand}</Link><nav id="primary-navigation" aria-label={copy.primaryNav}>{links.map(link => <Link key={link.href} href={link.href} className="nav-link" aria-current={pathname === link.href ? 'page' : undefined} onClick={() => setOpen(false)}><Icon name={link.icon} />{link.label}</Link>)}</nav><div className="sidebar-foot"><span className="demo-avatar">C</span><div>{copy.local}<small>CREAO Design Lab</small></div></div></aside><main id="main-content" tabIndex={-1}>{children}</main></div>;
}
