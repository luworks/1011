import { Button, Icon } from '@/components/ui';
export function EmptyState({ title, description, action, icon = 'files' }: { title: string; description: string; action: { label: string; onClick: () => void }; icon?: string }) {
  return <section className="empty-state"><div className="empty-icon"><Icon name={icon} size={28} /></div><h2>{title}</h2><p data-testid="empty-state-description">{description}</p><Button onClick={action.onClick}>{action.label}</Button></section>;
}
