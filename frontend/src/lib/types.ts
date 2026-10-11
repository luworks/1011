// Mirrors TurnResult / QuestionDecision in src/policy_agent (read-only view).
export type Evidence = {
  document_id: string;
  source_id: string;
  path: string;
  start_line: number;
  end_line: number;
  excerpt: string;
};

export type Decision = {
  question: string;
  policy_ids: string[];
  evidence: Evidence[];
  answer_status: "grounded" | "partial" | "needs_information" | "unsupported";
  action_status: "not_applicable" | "pending_verification" | "requires_human" | "eligible_for_simulation";
  reply: string;
  amount: string | null;
  conditions: Record<string, boolean | null>;
  missing: string[];
  reasons: string[];
};

export type Fact = {
  field: string;
  value: unknown;
  source_index: number;
  source_type: string;
  status: "confirmed" | "reported" | "unknown" | "conflicting";
  quote?: string;
};

export type CandidateQuestion = {
  intent: string;
  policy_ids: string[];
  amount: string | null;
  answer_status: string;
  action_status: string;
  tax_adjustment: string;
};

export type Turn = {
  turn: number;
  customer_input: string;
  candidate: { questions: CandidateQuestion[] } | null;
  decisions: Decision[];
  gate_errors: string[];
  error: string | null;
  retrieved: Evidence[];
  facts: Fact[];
  mode: string;
  reply: string;
  context: Record<string, unknown>;
  source_messages: { role: string; content: string }[];
  latency_seconds: number;
  understanding?: { intents: string[] } | null;
};

export type Usage = { calls: number; estimated_cost_usd: number };

export type Status = {
  corpus_entries: number;
  corpus_version: string;
  keys: { openai: boolean; anthropic: boolean };
  ledger_spent_usd: number;
  ledger_limit_usd: number;
  models: { config_id: string; provider: string; model: string; key_present: boolean }[];
  default_config_id: string;
  today: string;
};

export type RunInfo = { name: string; mode?: string; models?: string[]; prompt_version?: string };
