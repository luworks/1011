"use client";

import type { Decision, Turn } from "@/lib/types";

const TONE: Record<string, string> = {
  grounded: "good",
  eligible_for_simulation: "good",
  confirmed: "good",
  partial: "warn",
  pending_verification: "warn",
  needs_information: "warn",
  reported: "info",
  requires_human: "alert",
  unsupported: "alert",
  conflicting: "alert",
  technical_error: "alert",
  live: "info",
  offline_fixture: "muted",
};

export function StatusBadge({ value }: { value: string }) {
  return <span className={`badge tone-${TONE[value] ?? "muted"}`}>{value.replaceAll("_", " ")}</span>;
}

export function Inspector({ turn }: { turn: Turn | null }) {
  if (!turn) {
    return (
      <div className="inspector empty">
        <p>Select an agent reply to see how the decision was made:</p>
        <ol>
          <li>LLM understanding (intents + source-quoted facts)</li>
          <li>Retrieved policy sources</li>
          <li>Model candidate vs. deterministic policy gate</li>
          <li>Final decision, evidence and missing verification</li>
        </ol>
      </div>
    );
  }
  const intents = turn.understanding?.intents ?? [];
  return (
    <div className="inspector">
      <header className="inspector-head">
        <h2>Turn {turn.turn}</h2>
        <StatusBadge value={turn.mode} />
        <span className="muted">{turn.latency_seconds.toFixed(2)}s end-to-end</span>
      </header>

      {turn.error && (
        <div className="banner alert">
          Technical error: <code>{turn.error}</code>. No credit was issued.
          {turn.error === "BudgetExceeded" && " The shared ledger cap was reached (WEB_MAX_COST_USD)."}
        </div>
      )}

      <Section title="1 · Understanding">
        <div className="chips">
          {intents.length ? intents.map((i) => <span key={i} className="chip">{i}</span>) : <span className="muted">No billing intent</span>}
        </div>
      </Section>

      <Section title={`2 · Final decisions (${turn.decisions.length})`}>
        {turn.decisions.length === 0 && <p className="muted">No policy decision this turn.</p>}
        {turn.decisions.map((d, i) => (
          <DecisionCard key={i} d={d} />
        ))}
      </Section>

      <Section title="3 · Model candidate vs. policy gate">
        <CandidateTable turn={turn} />
        {turn.gate_errors.length > 0 && (
          <div className="gate">
            <strong>Gate corrections</strong>
            <p className="muted small">The model proposed something the reviewed rules did not accept; the gate&apos;s value was used.</p>
            <div className="chips">
              {turn.gate_errors.map((g, i) => <span key={i} className="chip alert">{g}</span>)}
            </div>
          </div>
        )}
      </Section>

      <Section title={`4 · Facts (${turn.facts.length})`}>
        <table className="grid">
          <thead>
            <tr><th>Field</th><th>Value</th><th>Status</th><th>Source</th></tr>
          </thead>
          <tbody>
            {turn.facts.map((f, i) => (
              <tr key={i}>
                <td><code>{f.field}</code></td>
                <td>{String(f.value ?? "—")}</td>
                <td><StatusBadge value={f.status} /></td>
                <td className="small">
                  {f.source_type}
                  {f.quote && <div className="quote">“{f.quote}”</div>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      <Section title={`5 · Retrieved sources (${turn.retrieved.length})`}>
        <div className="chips">
          {turn.retrieved.map((r) => <span key={r.source_id} className="chip">{r.source_id}</span>)}
        </div>
      </Section>

      <details className="raw">
        <summary>Raw turn JSON</summary>
        <pre>{JSON.stringify(turn, null, 2)}</pre>
      </details>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="section">
      <h3>{title}</h3>
      {children}
    </section>
  );
}

function DecisionCard({ d }: { d: Decision }) {
  const conditions = Object.entries(d.conditions ?? {});
  return (
    <div className="decision">
      <div className="decision-head">
        <span className="question">{d.question}</span>
        {d.amount && <span className="amount">${d.amount}</span>}
      </div>
      <div className="chips">
        <StatusBadge value={d.answer_status} />
        <StatusBadge value={d.action_status} />
        {d.policy_ids.map((p) => <span key={p} className="chip policy">{p}</span>)}
      </div>
      {d.missing.length > 0 && (
        <div className="row">
          <span className="label">Missing</span>
          <div className="chips">{d.missing.map((m) => <span key={m} className="chip warn">{m}</span>)}</div>
        </div>
      )}
      {conditions.length > 0 && (
        <div className="row">
          <span className="label">Checks</span>
          <div className="chips">
            {conditions.map(([k, v]) => (
              <span key={k} className={`chip ${v === true ? "good" : v === false ? "alert" : "muted"}`}>
                {v === true ? "✓" : v === false ? "✗" : "?"} {k}
              </span>
            ))}
          </div>
        </div>
      )}
      {d.reasons.map((r, i) => <p key={i} className="reason">{r}</p>)}
      {d.evidence.map((e, i) => (
        <details key={i} className="evidence">
          <summary>
            <strong>{e.source_id}</strong> <span className="muted small">{e.path.split("/").pop()}:{e.start_line}–{e.end_line}</span>
          </summary>
          <pre>{e.excerpt}</pre>
        </details>
      ))}
    </div>
  );
}

function CandidateTable({ turn }: { turn: Turn }) {
  const questions = turn.candidate?.questions ?? [];
  if (!questions.length) {
    return <p className="muted small">{turn.mode === "live" ? "No model candidate this turn." : "Offline fixture: no model candidate (recorded understanding only)."}</p>;
  }
  return (
    <table className="grid">
      <thead>
        <tr><th>Intent</th><th>Field</th><th>Model candidate</th><th>Gate final</th></tr>
      </thead>
      <tbody>
        {questions.flatMap((q) => {
          const d = turn.decisions.find((x) => x.question === q.intent);
          const rows: [string, string, string][] = [
            ["amount", q.amount ?? "—", d?.amount ?? "—"],
            ["answer", q.answer_status, d?.answer_status ?? "—"],
            ["action", q.action_status, d?.action_status ?? "—"],
            ["policies", q.policy_ids.join(", ") || "—", d?.policy_ids.join(", ") || "—"],
          ];
          return rows.map(([field, a, b], i) => (
            <tr key={q.intent + field} className={a !== b ? "diff" : ""}>
              {i === 0 && <td rowSpan={rows.length}><code>{q.intent}</code></td>}
              <td className="small">{field}</td>
              <td>{a}</td>
              <td>{b}</td>
            </tr>
          ));
        })}
      </tbody>
    </table>
  );
}
