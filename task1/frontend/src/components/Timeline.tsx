"use client";

import type { Turn } from "@/lib/types";
import { StatusBadge } from "./Inspector";

type Props = {
  turns: Turn[];
  selected: number | null;
  onSelect: (turn: number) => void;
  pending?: string | null;
};

// Rebuilds the chronological conversation from each turn's cumulative source_messages,
// so historical agent confirmations (replay) appear exactly where the workflow saw them.
export function Timeline({ turns, selected, onSelect, pending }: Props) {
  let seen = 0;
  return (
    <div className="timeline">
      {turns.map((t) => {
        const fresh = t.source_messages.slice(seen);
        seen = t.source_messages.length;
        const prior = fresh.slice(0, -1).filter((m) => m.role !== "customer");
        return (
          <div key={t.turn} className="turn-group">
            {prior.map((m, i) => (
              <div key={i} className={`bubble note role-${m.role}`}>
                <span className="who">{roleLabel(m.role)}</span>
                {m.content}
              </div>
            ))}
            <div className="bubble customer">
              <span className="who">Customer · turn {t.turn}</span>
              {t.customer_input}
            </div>
            <button
              className={`bubble agent ${selected === t.turn ? "selected" : ""} ${t.error ? "has-error" : ""}`}
              onClick={() => onSelect(t.turn)}
            >
              <span className="who">
                Agent
                <span className="meta">
                  {t.decisions.map((d, i) => (
                    <StatusBadge key={i} value={d.action_status} />
                  ))}
                  {t.error && <StatusBadge value="technical_error" />}
                  <span className="latency">{t.latency_seconds.toFixed(1)}s</span>
                </span>
              </span>
              <span className="reply">{t.reply}</span>
              <span className="hint">Click to inspect evidence →</span>
            </button>
          </div>
        );
      })}
      {pending && (
        <div className="turn-group">
          <div className="bubble customer">
            <span className="who">Customer</span>
            {pending}
          </div>
          <div className="bubble agent thinking">
            <span className="dots">Understanding → retrieving policy → gating decision</span>
          </div>
        </div>
      )}
    </div>
  );
}

function roleLabel(role: string) {
  if (role === "historical_agent") return "Historical agent (transcript evidence, not a new check)";
  if (role === "tool") return "Simulated tool result";
  return role;
}
