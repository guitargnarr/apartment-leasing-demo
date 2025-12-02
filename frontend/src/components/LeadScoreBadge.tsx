interface LeadScoreBadgeProps {
  score: number;
  showLabel?: boolean;
}

export function LeadScoreBadge({ score, showLabel = true }: LeadScoreBadgeProps) {
  const getScoreCategory = (score: number) => {
    if (score >= 80) return { label: 'Hot', color: 'bg-red-500/20 text-red-400 border-red-500/30' };
    if (score >= 50) return { label: 'Warm', color: 'bg-orange-500/20 text-orange-400 border-orange-500/30' };
    return { label: 'Cold', color: 'bg-blue-500/20 text-blue-400 border-blue-500/30' };
  };

  const { label, color } = getScoreCategory(score);

  return (
    <div className="flex items-center gap-2">
      <span
        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${color}`}
      >
        {Math.round(score)}
      </span>
      {showLabel && (
        <span className="text-xs text-slate-400">{label}</span>
      )}
    </div>
  );
}
