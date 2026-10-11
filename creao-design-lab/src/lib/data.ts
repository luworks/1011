export type DemoFile = { id: string; name: string; modified: string; size: string; source: string; kind: 'document' | 'folder' | 'image'; content: string };
export const initialFiles: DemoFile[] = [
  { id: 'research', name: 'Quarterly research summary.md', modified: 'Oct 11, 10:30', size: '12 KB', source: 'Demo file', kind: 'document', content: 'Quarterly research summary\n\nKey finding: a consistent page structure helps the team deliver a consistent experience.\nOpen question: empty states and recovery actions across different tasks.' },
  { id: 'brief', name: 'Product requirements and design review notes.md', modified: 'Oct 10, 16:45', size: '24 KB', source: 'Demo file', kind: 'document', content: 'Design review notes\n\nPage titles, primary actions, search and content lists need a stable hierarchy.' },
  { id: 'workspace', name: 'Team workspace layout sketch.svg', modified: 'Oct 10, 11:20', size: '8 KB', source: 'Demo file', kind: 'image', content: 'Layout sketch example: navigation / page title / action bar / content.' },
  { id: 'long', name: 'Cross-team collaboration project long-term research materials and open items summary.md', modified: 'Oct 9, 09:15', size: '32 KB', source: 'Demo file', kind: 'document', content: 'Long filename case: verifies the full name stays reachable on narrow screens.' },
];
export const connectorCatalog = [
  { id: 'slack', name: 'Slack', mark: 'S', description: 'Share progress and organize discussions in team channels.' },
  { id: 'drive', name: 'Google Drive', mark: 'D', description: 'Find project documents and keep materials within reach.' },
  { id: 'notion', name: 'Notion', mark: 'N', description: 'Organize knowledge bases and project notes.' },
];
