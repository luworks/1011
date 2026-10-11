export type DemoFile = { id: string; name: string; modified: string; size: string; source: string; kind: 'document' | 'folder' | 'image'; content: string };
export const initialFiles: DemoFile[] = [
  { id: 'research', name: '季度研究摘要.md', modified: '10月11日 10:30', size: '12 KB', source: '演示文件', kind: 'document', content: '本季度研究摘要\n\n关键发现：统一页面结构有助于团队交付一致体验。\n待确认：不同任务中的空状态与恢复操作。' },
  { id: 'brief', name: '产品需求与设计评审记录.md', modified: '10月10日 16:45', size: '24 KB', source: '演示文件', kind: 'document', content: '设计评审记录\n\n页面标题、主要操作、搜索与内容列表需要保持稳定的层级。' },
  { id: 'workspace', name: '团队工作空间布局草图.svg', modified: '10月10日 11:20', size: '8 KB', source: '演示文件', kind: 'image', content: '布局草图示例：导航 / 页面标题 / 操作栏 / 内容。' },
  { id: 'long', name: '跨团队协作项目的长期研究资料与待确认事项汇总.md', modified: '10月9日 09:15', size: '32 KB', source: '演示文件', kind: 'document', content: '长文件名用例，验证窄屏下仍可获取完整名称。' },
];
export const connectorCatalog = [
  { id: 'slack', name: 'Slack', mark: 'S', description: '在团队频道中分享进展、整理讨论。' },
  { id: 'drive', name: 'Google Drive', mark: 'D', description: '查找项目文档，让资料触手可及。' },
  { id: 'notion', name: 'Notion', mark: 'N', description: '整理知识库与项目笔记。' },
];
