import type { UnitStatus } from '../types';

interface StatusBadgeProps {
  status: UnitStatus;
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const styles = {
    available: 'bg-teal-500/20 text-teal-400 border-teal-500/30',
    pending: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
    leased: 'bg-slate-500/20 text-slate-400 border-slate-500/30',
  };

  const labels = {
    available: 'Available',
    pending: 'Pending',
    leased: 'Leased',
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${styles[status]}`}
    >
      {labels[status]}
    </span>
  );
}
