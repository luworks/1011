import type { Metadata } from 'next';
import { Shell } from '@/components/patterns/Shell';
import '@/styles/tokens.css';
import '@/styles/components.css';
import '@/styles/layouts.css';
export const metadata: Metadata = { title: 'CREAO Design Lab', description: 'A local design governance prototype with synthetic data.' };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body><Shell>{children}</Shell></body></html>; }
