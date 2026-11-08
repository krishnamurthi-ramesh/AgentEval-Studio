export interface ExpectedToolCall {
  tool_name: string;
  arguments: Record<string, any>;
  is_high_risk?: boolean;
  required_arguments?: string[];
}

export interface RubricCriterion {
  name: string;
  description: string;
  weight: number;
  pass_rule?: string;
}

export interface EvalCase {
  id: string;
  category: string;
  user_input: string;
  expected_trajectory: ExpectedToolCall[];
  forbidden_tools?: string[];
  tags: string[];
  metadata?: Record<string, any>;
}

export interface EvalPack {
  id: string;
  name: string;
  version: string;
  author: string;
  description: string;
  category: string;
  cases: EvalCase[];
  rubrics: RubricCriterion[];
  tags: string[];
  recommended_gates?: {
    min_tool_accuracy?: number;
    max_latency_regression_pct?: number;
    zero_tolerance_tools?: string[];
  };
}

export interface ActualToolCall {
  tool_name: string;
  arguments: Record<string, any>;
  execution_success?: boolean;
  output?: any;
}

export interface RowScorecard {
  case_id: string;
  variant_name: string;
  tool_selection_score: number;
  schema_score: number;
  argument_score: number;
  trajectory_score: number;
  passed: boolean;
  is_high_risk_failure: boolean;
  diagnostic_notes: string[];
}

export interface VariantScorecard {
  variant_name: string;
  total_cases: number;
  passed_cases: number;
  pass_rate: number;
  avg_tool_accuracy: number;
  avg_argument_score: number;
  avg_trajectory_score: number;
  p50_latency_ms: number;
  p90_latency_ms: number;
  total_cost_usd: number;
  high_risk_failures: number;
  rows: RowScorecard[];
}

export interface GateResult {
  gate_name: string;
  passed: boolean;
  threshold: any;
  actual_value: any;
  is_hard_blocker: boolean;
  message: string;
}

export interface ReleaseGatePolicy {
  min_pass_rate: number;
  min_tool_accuracy: number;
  min_argument_score: number;
  min_trajectory_score: number;
  max_latency_regression_pct: number;
  max_cost_regression_pct: number;
  zero_tolerance_tools: string[];
}

export interface ReleaseDecisionBrief {
  candidate_variant: string;
  baseline_variant?: string;
  status: 'READY_TO_SHIP' | 'BLOCKED' | 'REQUIRES_REVIEW';
  gates_evaluated: GateResult[];
  total_gates: number;
  passed_gates: number;
  failed_gates: number;
  hard_blockers: string[];
  trade_offs_summary: string;
  markdown_content: string;
}
