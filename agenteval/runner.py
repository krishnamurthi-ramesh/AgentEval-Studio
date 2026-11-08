"""
Evaluation Runner for AgentEval Studio.
Executes Eval Packs against agent variants and produces row-level and aggregated scorecards.
"""

from typing import List, Dict, Any, Callable, Optional
import time
import numpy as np
from agenteval.models import (
    EvalPack,
    EvalCase,
    AgentRunResult,
    RowScorecard,
    VariantScorecard,
    ActualToolCall,
)
from agenteval.evaluators.tool_selection import ToolSelectionEvaluator
from agenteval.evaluators.schema_validator import SchemaValidator
from agenteval.evaluators.argument_match import ArgumentMatchEvaluator
from agenteval.evaluators.trajectory import TrajectoryEvaluator


class EvalRunner:
    """
    Executes and scores agent execution results against an EvalPack.
    """

    def __init__(self):
        self.tool_evaluator = ToolSelectionEvaluator()
        self.schema_evaluator = SchemaValidator()
        self.arg_evaluator = ArgumentMatchEvaluator()
        self.trajectory_evaluator = TrajectoryEvaluator()

    def score_run(
        self,
        pack: EvalPack,
        runs: List[AgentRunResult],
        variant_name: str,
        high_risk_tool_names: Optional[List[str]] = None
    ) -> VariantScorecard:
        """Score a list of pre-collected agent execution traces against an EvalPack."""
        case_map: Dict[str, EvalCase] = {c.id: c for c in pack.cases}
        row_scorecards: List[RowScorecard] = []
        high_risk_tool_names = high_risk_tool_names or [
            "transfer_funds", "freeze_debit_card", "dispute_charge", "issue_refund", "cancel_order"
        ]

        latencies: List[float] = []
        total_cost = 0.0

        for run in runs:
            case = case_map.get(run.case_id)
            if not case:
                continue

            latencies.append(run.latency_ms)
            total_cost += run.cost_usd

            # 1. Tool Selection
            tool_score, tool_notes = self.tool_evaluator.evaluate(
                actual=run.actual_trajectory,
                expected=case.expected_trajectory,
                forbidden_tools=case.forbidden_tools
            )

            # 2. Schema Validation
            schema_score, schema_notes = self.schema_evaluator.evaluate(
                actual=run.actual_trajectory,
                expected=case.expected_trajectory
            )

            # 3. Argument Correctness
            arg_score, arg_notes = self.arg_evaluator.evaluate(
                actual=run.actual_trajectory,
                expected=case.expected_trajectory
            )

            # 4. Trajectory Flow
            traj_score, traj_notes = self.trajectory_evaluator.evaluate(
                actual=run.actual_trajectory,
                expected=case.expected_trajectory
            )

            # Combine diagnostics
            all_notes = tool_notes + schema_notes + arg_notes + traj_notes

            # Row pass criteria: high tool accuracy and good arguments
            passed = (tool_score >= 0.8) and (schema_score >= 0.8) and (arg_score >= 0.8)

            # Check if this failure affected a high-risk tool
            is_high_risk_failure = False
            if not passed:
                for exp_tool in case.expected_trajectory:
                    if exp_tool.is_high_risk or exp_tool.tool_name in high_risk_tool_names:
                        is_high_risk_failure = True
                        break

            row_card = RowScorecard(
                case_id=run.case_id,
                variant_name=variant_name,
                tool_selection_score=tool_score,
                schema_score=schema_score,
                argument_score=arg_score,
                trajectory_score=traj_score,
                passed=passed,
                is_high_risk_failure=is_high_risk_failure,
                diagnostic_notes=all_notes
            )
            row_scorecards.append(row_card)

        total_cases = len(row_scorecards)
        passed_cases = sum(1 for r in row_scorecards if r.passed)
        high_risk_count = sum(1 for r in row_scorecards if r.is_high_risk_failure)

        avg_tool = float(np.mean([r.tool_selection_score for r in row_scorecards])) if row_scorecards else 0.0
        avg_arg = float(np.mean([r.argument_score for r in row_scorecards])) if row_scorecards else 0.0
        avg_traj = float(np.mean([r.trajectory_score for r in row_scorecards])) if row_scorecards else 0.0

        p50_lat = float(np.percentile(latencies, 50)) if latencies else 0.0
        p90_lat = float(np.percentile(latencies, 90)) if latencies else 0.0

        return VariantScorecard(
            variant_name=variant_name,
            total_cases=total_cases,
            passed_cases=passed_cases,
            pass_rate=round(passed_cases / total_cases, 3) if total_cases > 0 else 0.0,
            avg_tool_accuracy=round(avg_tool, 3),
            avg_argument_score=round(avg_arg, 3),
            avg_trajectory_score=round(avg_traj, 3),
            p50_latency_ms=round(p50_lat, 1),
            p90_latency_ms=round(p90_lat, 1),
            total_cost_usd=round(total_cost, 4),
            high_risk_failures=high_risk_count,
            rows=row_scorecards
        )

    def evaluate_agent(
        self,
        pack: EvalPack,
        agent_fn: Callable[[str], Dict[str, Any]],
        variant_name: str
    ) -> VariantScorecard:
        """
        Execute an agent callable across all cases in an EvalPack and score it.
        agent_fn signature: takes user_input (str), returns Dict with:
            {
               "trajectory": [{"tool_name": str, "arguments": dict}],
               "final_response": str,
               "tokens": {"prompt": int, "completion": int} (optional)
            }
        """
        runs: List[AgentRunResult] = []
        for case in pack.cases:
            t0 = time.perf_counter()
            try:
                res = agent_fn(case.user_input)
                elapsed_ms = (time.perf_counter() - t0) * 1000.0

                raw_traj = res.get("trajectory", [])
                actual_traj = [
                    ActualToolCall(
                        tool_name=step["tool_name"],
                        arguments=step.get("arguments", {})
                    )
                    for step in raw_traj
                ]
                tokens = res.get("tokens", {})
                p_tok = tokens.get("prompt", 150)
                c_tok = tokens.get("completion", 60)
                # Estimate cost (~$0.003/1k tokens)
                cost = (p_tok * 0.0000015) + (c_tok * 0.000005)

                runs.append(
                    AgentRunResult(
                        case_id=case.id,
                        variant_name=variant_name,
                        actual_trajectory=actual_traj,
                        final_response=res.get("final_response", ""),
                        latency_ms=elapsed_ms,
                        prompt_tokens=p_tok,
                        completion_tokens=c_tok,
                        cost_usd=cost
                    )
                )
            except Exception as e:
                elapsed_ms = (time.perf_counter() - t0) * 1000.0
                runs.append(
                    AgentRunResult(
                        case_id=case.id,
                        variant_name=variant_name,
                        actual_trajectory=[],
                        final_response=f"Error executing agent: {str(e)}",
                        latency_ms=elapsed_ms,
                        error=str(e)
                    )
                )

        return self.score_run(pack, runs, variant_name)
