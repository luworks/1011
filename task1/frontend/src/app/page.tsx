"use client";

import { useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";
import type { RunInfo, Status, Turn, Usage } from "@/lib/types";
import { Timeline } from "@/components/Timeline";
import { Inspector, StatusBadge } from "@/components/Inspector";

type Tab = "chat" | "replay" | "runs";

const PRESETS = [
  "Hi, I need to dispute a charge on my latest bill. My service was out for almost two weeks last month and I still got charged the full $225.00 like nothing happened.",
  "Service went down on September 10th at 6 AM and wasn't back until September 21st at 6 AM — all three lines, totally dead. I'm disputing the full $225.00 recurring charge on the invoice dated October 1st.",
  "Isn't your refund limit only $75? So you can only give me $75 back for this, right?",
  "Does the credit also reduce the taxes and regulatory surcharges I paid during those eleven days?",
  "How long do I have to submit a request like this after an outage gets fixed?",
];

const EXAMPLE_CONTEXT = `{
  "monthly_charge": "225.00"
}`;

export default function Home() {
  const [tab, setTab] = useState<Tab>("chat");
  const [status, setStatus] = useState<Status | null>(null);
  const [statusError, setStatusError] = useState<string | null>(null);

  const refreshStatus = () =>
    api<Status>("/status")
      .then((s) => {
        setStatus(s);
        setStatusError(null);
      })
      .catch((e) => setStatusError(e.message));

  useEffect(() => {
    refreshStatus();
  }, []);

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="logo">◆</span>
          <div>
            <h1>Policy Agent Console</h1>
            <p className="muted small">Nimbus Wireless billing · evidence-bounded agent · local simulation, no real credits or handoffs</p>
          </div>
        </div>
        <nav className="tabs">
          {(
            [
              ["chat", "Live chat"],
              ["replay", "Transcript replay"],
              ["runs", "Recorded runs"],
            ] as [Tab, string][]
          ).map(([key, label]) => (
            <button key={key} className={tab === key ? "active" : ""} onClick={() => setTab(key)}>
              {label}
            </button>
          ))}
        </nav>
        <StatusPill status={status} error={statusError} />
      </header>

      {statusError && (
        <div className="banner alert page-banner">
          Cannot reach the Python bridge ({statusError}). Start it with <code>uv run --frozen python scripts/web_api.py</code>.
        </div>
      )}

      <main className="main">
        {tab === "chat" && <ChatView status={status} onSpend={refreshStatus} />}
        {tab === "replay" && <ReplayView status={status} onSpend={refreshStatus} />}
        {tab === "runs" && <RunsView />}
      </main>
    </div>
  );
}

function StatusPill({ status, error }: { status: Status | null; error: string | null }) {
  if (error) return <div className="pill alert">Bridge offline</div>;
  if (!status) return <div className="pill">Connecting…</div>;
  return (
    <div className="pill" title={`Corpus ${status.corpus_version.slice(0, 12)}`}>
      <span>{status.corpus_entries} policy sources</span>
      <span className="sep" />
      <span>
        Ledger ${status.ledger_spent_usd.toFixed(2)} / ${status.ledger_limit_usd.toFixed(0)}
      </span>
    </div>
  );
}

function Workspace({
  turns,
  pending,
  footer,
  empty,
}: {
  turns: Turn[];
  pending?: string | null;
  footer?: React.ReactNode;
  empty?: React.ReactNode;
}) {
  const [selected, setSelected] = useState<number | null>(null);
  const last = turns.length ? turns[turns.length - 1].turn : null;
  // Follow the newest turn unless the user picked one explicitly.
  useEffect(() => setSelected(last), [last]);
  const current = useMemo(() => turns.find((t) => t.turn === selected) ?? null, [turns, selected]);
  return (
    <div className="workspace">
      <div className="conversation">
        <div className="scroll">
          {turns.length === 0 && !pending ? empty : <Timeline turns={turns} selected={selected} onSelect={setSelected} pending={pending} />}
        </div>
        {footer}
      </div>
      <aside className="side">
        <Inspector turn={current} />
      </aside>
    </div>
  );
}

function ModelSelect({ status, value, onChange }: { status: Status | null; value: string; onChange: (v: string) => void }) {
  return (
    <select value={value} onChange={(e) => onChange(e.target.value)} disabled={!status}>
      {status?.models.map((m) => (
        <option key={m.config_id} value={m.config_id} disabled={!m.key_present}>
          {m.config_id}
          {m.key_present ? "" : " (no key)"}
        </option>
      ))}
    </select>
  );
}

function ChatView({ status, onSpend }: { status: Status | null; onSpend: () => void }) {
  const [configId, setConfigId] = useState("");
  const [date, setDate] = useState("2026-10-05");
  const [contextText, setContextText] = useState(EXAMPLE_CONTEXT);
  const [session, setSession] = useState<{ id: string; config: string; runDir: string } | null>(null);
  const [turns, setTurns] = useState<Turn[]>([]);
  const [input, setInput] = useState("");
  const [pending, setPending] = useState<string | null>(null);
  const [usage, setUsage] = useState<Usage | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (status && !configId) setConfigId(status.default_config_id);
  }, [status, configId]);

  async function start() {
    setError(null);
    let context: unknown = {};
    try {
      context = contextText.trim() ? JSON.parse(contextText) : {};
    } catch {
      setError("Account context must be valid JSON");
      return;
    }
    try {
      const s = await api<{ session_id: string; config_id: string; run_dir: string }>("/session", {
        config_id: configId,
        date,
        context,
      });
      setSession({ id: s.session_id, config: s.config_id, runDir: s.run_dir });
      setTurns([]);
      setUsage(null);
    } catch (e) {
      setError((e as Error).message);
    }
  }

  async function send(text: string) {
    if (!session || !text.trim() || pending) return;
    setPending(text);
    setInput("");
    setError(null);
    try {
      const r = await api<{ result: Turn; usage: Usage }>("/turn", { session_id: session.id, text });
      setTurns((t) => [...t, r.result]);
      setUsage(r.usage);
    } catch (e) {
      setError((e as Error).message);
      setInput(text);
    } finally {
      setPending(null);
      onSpend();
    }
  }

  if (!session) {
    return (
      <div className="setup card">
        <h2>Start a live conversation</h2>
        <p className="muted">
          Each customer turn calls the selected model through your local <code>.env</code> keys, then the deterministic policy gate decides. Calls are
          charged to the demo ledger <code>runs/web-budget.json</code>; turns are saved under <code>runs/web-chat-*</code>.
        </p>
        <label>
          Model configuration
          <ModelSelect status={status} value={configId} onChange={setConfigId} />
        </label>
        <label>
          Request date
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
        </label>
        <label>
          Simulated account context (JSON, treated as a verified account record)
          <textarea rows={5} value={contextText} onChange={(e) => setContextText(e.target.value)} spellCheck={false} />
          <span className="muted small">
            Fields: monthly_charge, outage_start, outage_end, statement_date, ticket_status, address_matches, history_checked, fraud, identity_verified,
            line_item… Leave <code>{"{}"}</code> for an unverified customer.
          </span>
        </label>
        {error && <div className="banner alert">{error}</div>}
        <button className="primary" onClick={start} disabled={!status || !configId}>
          Start conversation
        </button>
      </div>
    );
  }

  return (
    <Workspace
      turns={turns}
      pending={pending}
      empty={
        <div className="empty-chat">
          <p>Session ready with <code>{session.config}</code>. Try a message from the original transcript:</p>
        </div>
      }
      footer={
        <div className="composer">
          <div className="presets">
            {PRESETS.map((p) => (
              <button key={p} className="chip button" onClick={() => send(p)} disabled={!!pending} title={p}>
                {p.length > 48 ? p.slice(0, 48) + "…" : p}
              </button>
            ))}
          </div>
          {error && <div className="banner alert">{error}</div>}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              send(input);
            }}
          >
            <textarea
              rows={2}
              placeholder="Type a customer message… (Enter to send, Shift+Enter for newline)"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
                  e.preventDefault();
                  send(input);
                }
              }}
              disabled={!!pending}
            />
            <button className="primary" type="submit" disabled={!!pending || !input.trim()}>
              {pending ? "Thinking…" : "Send"}
            </button>
          </form>
          <div className="composer-meta muted small">
            <span>{session.config}</span>
            {usage && (
              <span>
                {usage.calls} model calls · est. ${usage.estimated_cost_usd.toFixed(4)}
              </span>
            )}
            <span>{session.runDir}</span>
            <button className="link" onClick={() => setSession(null)}>
              New conversation
            </button>
          </div>
        </div>
      }
    />
  );
}

function ReplayView({ status, onSpend }: { status: Status | null; onSpend: () => void }) {
  const [mode, setMode] = useState<"offline" | "live">("offline");
  const [configId, setConfigId] = useState("");
  const [turns, setTurns] = useState<Turn[]>([]);
  const [meta, setMeta] = useState<{ mode: string; runDir: string; usage: Usage } | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (status && !configId) setConfigId(status.default_config_id);
  }, [status, configId]);

  async function run() {
    setBusy(true);
    setError(null);
    try {
      const r = await api<{ mode: string; run_dir: string; turns: Turn[]; usage: Usage }>("/replay", { mode, config_id: configId });
      setTurns(r.turns);
      setMeta({ mode: r.mode, runDir: r.run_dir, usage: r.usage });
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
      onSpend();
    }
  }

  return (
    <div className="stack">
      <div className="toolbar card">
        <div>
          <strong>Dana Whitfield · October 5, 2026</strong>
          <p className="muted small">The supplied transcript processed chronologically. Historical agent messages are evidence, not new backend checks.</p>
        </div>
        <div className="controls">
          <div className="segmented">
            <button className={mode === "offline" ? "active" : ""} onClick={() => setMode("offline")}>
              Offline fixture
            </button>
            <button className={mode === "live" ? "active" : ""} onClick={() => setMode("live")}>
              Live model
            </button>
          </div>
          {mode === "live" && <ModelSelect status={status} value={configId} onChange={setConfigId} />}
          <button className="primary" onClick={run} disabled={busy}>
            {busy ? (mode === "live" ? "Running live (~1 min)…" : "Running…") : "Run replay"}
          </button>
        </div>
      </div>
      {mode === "offline" && (
        <p className="muted small note-line">Offline fixture uses recorded understanding for this transcript only: it is not an LLM evaluation and costs nothing.</p>
      )}
      {error && <div className="banner alert">{error}</div>}
      {meta && (
        <div className="muted small note-line">
          <StatusBadge value={meta.mode} /> {meta.usage.calls} model calls · est. ${meta.usage.estimated_cost_usd.toFixed(4)} · saved to{" "}
          <code>{meta.runDir}</code>
        </div>
      )}
      <Workspace turns={turns} empty={<div className="empty-chat">Run the replay to see all six customer turns.</div>} />
    </div>
  );
}

function RunsView() {
  const [runs, setRuns] = useState<RunInfo[]>([]);
  const [name, setName] = useState("");
  const [data, setData] = useState<{ turns: Turn[]; models: string[]; manifest: Record<string, string>; usage: Usage } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api<{ runs: RunInfo[] }>("/runs")
      .then((r) => setRuns(r.runs))
      .catch((e) => setError(e.message));
  }, []);

  useEffect(() => {
    if (!name) return;
    setData(null);
    api<{ turns: Turn[]; models: string[]; manifest: Record<string, string>; usage: Usage }>(`/runs/${encodeURIComponent(name)}`)
      .then(setData)
      .catch((e) => setError(e.message));
  }, [name]);

  return (
    <div className="stack">
      <div className="toolbar card">
        <div>
          <strong>Recorded runs</strong>
          <p className="muted small">Read-only traces from <code>runs/</code> (replay and chat). Recorded traces are evidence of that snapshot, not a model ranking.</p>
        </div>
        <select value={name} onChange={(e) => setName(e.target.value)}>
          <option value="">Select a run…</option>
          {runs.map((r) => (
            <option key={r.name} value={r.name}>
              {r.name} · {r.mode ?? "?"} {r.models?.length ? `· ${r.models.join(", ")}` : ""} {r.prompt_version ? `· ${r.prompt_version}` : ""}
            </option>
          ))}
        </select>
      </div>
      {error && <div className="banner alert">{error}</div>}
      {data && (
        <div className="muted small note-line">
          <StatusBadge value={data.manifest.mode ?? "recorded"} /> {data.models.join(", ") || "no model"} · {data.manifest.prompt_version} · {data.usage.calls}{" "}
          calls · est. ${data.usage.estimated_cost_usd.toFixed(4)}
        </div>
      )}
      <Workspace turns={data?.turns ?? []} empty={<div className="empty-chat">Pick a run to inspect its turns.</div>} />
    </div>
  );
}
