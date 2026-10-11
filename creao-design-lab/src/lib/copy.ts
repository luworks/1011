export const copy = {
  brand: 'CREAO', local: '本地交互原型', skip: '跳到主要内容', menu: '切换导航',
  nav: { files: '文件', connectors: '连接器', agents: '智能体', guidelines: '设计规范' },
  files: { title: '文件', search: '搜索文件和文件夹', clear: '清除搜索', create: '新建文件夹', folderName: '文件夹名称', save: '创建文件夹', cancel: '取消', list: '列表视图', grid: '网格视图', name: '名称', modified: '修改时间', size: '大小', source: '来源', emptyTitle: '没有找到文件', emptyDescription: '试试其他关键词，或清除搜索查看所有文件。', preview: '预览', close: '关闭预览', folder: '文件夹', created: '已创建文件夹', invalid: '请输入文件夹名称。', duplicate: '已存在同名文件夹，请换一个名称。', demo: '演示文件', previewNote: '此内容为合成演示数据，文件操作仅在当前页面保留。' },
  connectors: { title: '连接器', description: '将日常工具带入你的工作流程。', all: '全部', available: '可连接', connected: '已连接', search: '搜索连接器', emptyTitle: '暂无已连接的连接器', recover: '浏览可连接服务', connect: '模拟连接', disconnect: '取消模拟连接', demo: '仅本地演示，不会访问第三方账号。', noResults: '没有找到连接器', clear: '清除搜索', categories: '精选连接器', count: '个结果' },
  agents: { title: '智能体', emptyTitle: '创建你的第一个智能体', emptyDescription: '让智能体协助整理资料、跟进工作。先查看一个本地示例。', create: '创建示例智能体', name: '研究助手', description: '整理公开资料，并提供可追溯的摘要。', demo: '本地示例，不调用模型或外部服务。', back: '返回智能体列表', details: '查看详情', status: '草稿', detailTitle: '研究助手', task: '工作说明', body: '接收一个研究主题，整理相关资料，列出来源与待确认的问题。', run: '预览示例结果', resultTitle: '示例结果', result: '摘要结构：关键发现、来源清单、待确认事项。这是预先写好的示例。' },
  guidelines: { title: '设计规范', description: '本地适配规范与执行入口。规则是否通过，以实际检查报告为准。' },
} as const;
