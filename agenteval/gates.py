"""
Release Policy Gate Engine for AgentEval Studio.
Evaluates agent candidate variants against baseline and business policy thresholds.
"""

from typing import Optional, List
from agenteval.models import (
    VariantScorecard,
    ReleaseGatePolicy,
    GateResult,
    ReleaseDecisionBrief,
)


class PolicyGateEngine:
    """
    Evaluates an agent variant's scorecard against explicit release criteria gates.
    """

    def __init__(self, policy: Optional[ReleaseGatePolicy] = None):
        self.policy = policy or ReleaseGatePolicy()

    def evaluate_release(
        self,
        candidate: VariantScorecard,
        baseline: Optional[VariantScorecard] = None,
    ) -> ReleaseDecisionBrief:
        gate_results: List[GateResult] = []
        hard_blockers: List[str] = []

        # Gate 1: High-Risk Tool Blocker
        high_risk_failed = candidate.high_risk_failures > 0
        if high_risk_failed:
            hard_blockers.append(
                f"High-risk tool failure: {candidate.high_risk_failures} catastrophic errors detected on sensitive tools."
            )
            gate_results.append(
                GateResult(
                    gate_name="Zero-Tolerance High-Risk Tools",
                    passed=False,
                    threshold=0,
                    actual_value=candidate.high_risk_failures,
                    is_hard_blocker=True,
                    message=f"FAILED: Detected {candidate.high_risk_failures} high-risk tool failure(s)."
                )
            )
        else:
            gate_results.append(
                GateResult(
                    gate_name="Zero-Tolerance High-Risk Tools",
                    passed=True,
                    threshold=0,
                    actual_value=0,
                    is_hard_blocker=True,
                    message="PASSED: Zero failures on high-risk tools."
                )
            )

        # Gate 2: Tool Selection Accuracy
        tool_passed = candidate.avg_tool_accuracy >= self.policy.min_tool_accuracy
        gate_results.append(
            GateResult(
                gate_name="Tool Selection Accuracy",
                passed=tool_passed,
                threshold=self.policy.min_tool_accuracy,
                actual_value=round(candidate.avg_tool_accuracy, 3),
                is_hard_blocker=False,
                message=f"{'PASSED' if tool_passed else 'FAILED'}: Accuracy {candidate.avg_tool_accuracy:.1%} (Threshold: {self.policy.min_tool_accuracy:.1%})"
            )
        )

        # Gate 3: Argument Correctness
        arg_passed = candidate.avg_argument_score >= self.policy.min_argument_score
        gate_results.append(
            GateResult(
                gate_name="Argument Entity Correctness",
                passed=arg_passed,
                threshold=self.policy.min_argument_score,
                actual_value=round(candidate.avg_argument_score, 3),
                is_hard_blocker=False,
                message=f"{'PASSED' if arg_passed else 'FAILED'}: Score {candidate.avg_argument_score:.1%} (Threshold: {self.policy.min_argument_score:.1%})"
            )
        )

        # Gate 4: Overall Pass Rate
        pass_rate_passed = candidate.pass_rate >= self.policy.min_pass_rate
        gate_results.append(
            GateResult(
                gate_name="Benchmark Pass Rate",
                passed=pass_rate_passed,
                threshold=self.policy.min_pass_rate,
                actual_value=round(candidate.pass_rate, 3),
                is_hard_blocker=False,
                message=f"{'PASSED' if pass_rate_passed else 'FAILED'}: Pass Rate {candidate.pass_rate:.1%} (Threshold: {self.policy.min_pass_rate:.1%})"
            )
        )

        # Gate 5: Latency Regression (vs Baseline)
        if baseline and baseline.p50_latency_ms > 0:
            lat_delta_pct = (
                (candidate.p50_latency_ms - baseline.p50_latency_ms) / baseline.p50_latency_ms
            ) * 100.0
            lat_passed = lat_delta_pct <= self.policy.max_latency_regression_pct
            gate_results.append(
                GateResult(
                    gate_name="Latency Regression Ceiling",
                    passed=lat_passed,
                    threshold=f"+{self.policy.max_latency_regression_pct}%",
                    actual_value=f"{lat_delta_pct:+.1f}% ({candidate.p50_latency_ms:.0f}ms vs {baseline.p50_latency_ms:.0f}ms)",
                    is_hard_blocker=False,
                    message=f"{'PASSED' if lat_passed else 'REGRESSION'}: Latency changed by {lat_delta_pct:+.1f}%"
                )
            )

        # Gate 6: Cost Regression (vs Baseline)
        if baseline and baseline.total_cost_usd > 0:
            cost_delta_pct = (
                (candidate.total_cost_usd - baseline.total_cost_usd) / baseline.total_cost_usd
            ) * 100.0
            cost_passed = cost_delta_pct <= self.policy.max_cost_regression_pct
            gate_results.append(
                GateResult(
                    gate_name="Cost Regression Ceiling",
                    passed=cost_passed,
                    threshold=f"+{self.policy.max_cost_regression_pct}%",
                    actual_value=f"{cost_delta_pct:+.1f}% (${candidate.total_cost_usd:.4f} vs ${baseline.total_cost_usd:.4f})",
                    is_hard_blocker=False,
                    message=f"{'PASSED' if cost_passed else 'REGRESSION'}: Cost changed by {cost_delta_pct:+.1f}%"
                )
            )

        # Calculate Status
        passed_count = sum(1 for g in gate_results if g.passed)
        failed_count = len(gate_results) - passed_count

        if hard_blockers or failed_count >= 2:
            status = "BLOCKED"
        elif failed_count == 1:
            status = "REQUIRES_REVIEW"
        else:
            status = "READY_TO_SHIP"

        # Trade-offs summary
        trade_offs = []
        if baseline:
            acc_diff = (candidate.avg_tool_accuracy - baseline.avg_tool_accuracy) * 100.0
            trade_offs.append(f"Tool Accuracy: {acc_diff:+.1f}%")
            lat_diff = candidate.p50_latency_ms - baseline.p50_latency_ms
            trade_offs.append(f"Latency Delta: {lat_diff:+.0f}ms")
            cost_diff = candidate.total_cost_usd - baseline.total_cost_usd
            trade_offs.append(f"Cost Delta: ${cost_diff:+.4f}")

        # Failing cases summary
        failing_cases = []
        for row in candidate.rows:
            if not row.passed:
                failing_cases.append({
                    "case_id": row.case_id,
                    "is_high_risk": row.is_high_risk_failure,
                    "diagnostics": "; ".join(row.diagnostic_notes)
                })

        brief = ReleaseDecisionBrief(
            candidate_variant=candidate.variant_name,
            baseline_variant=baseline.variant_name if baseline else None,
            status=status,
            gates_evaluated=gate_results,
            total_gates=len(gate_results),
            passed_gates=passed_count,
            failed_gates=failed_count,
            hard_blockers=hard_blockers,
            trade_offs_summary=" | ".join(trade_offs) if trade_offs else "No baseline comparison",
            failing_cases_summary=failing_cases
        )

        # Generate Markdown version
        brief.markdown_content = self.render_markdown_brief(brief, candidate, baseline)
        return brief

    def render_markdown_brief(
        self,
        brief: ReleaseDecisionBrief,
        candidate: VariantScorecard,
        baseline: Optional[VariantScorecard] = None
    ) -> str:
        status_badges = {
            "READY_TO_SHIP": "🟢 READY TO SHIP",
            "REQUIRES_REVIEW": "🟡 REQUIRES PM EXCEPTION REVIEW",
            "BLOCKED": "🔴 RELEASE BLOCKED BY POLICY REGRESSION"
        }

        md = [
            f"# Release Decision Brief — {candidate.variant_name}",
            f"**Recommendation Status:** {status_badges.get(brief.status, brief.status)}",
            f"**Candidate:** `{candidate.variant_name}` | **Baseline:** `{baseline.variant_name if baseline else 'None'}`",
            f"**Gates Passed:** {brief.passed_gates} / {brief.total_gates}\n",
            "---",
            "## 1. Executive Summary & Trade-Offs",
            f"- **Overall Pass Rate:** {candidate.pass_rate:.1%} ({candidate.passed_cases}/{candidate.total_cases})",
            f"- **Tool Selection Accuracy:** {candidate.avg_tool_accuracy:.1%}",
            f"- **Argument Entity Correctness:** {candidate.avg_argument_score:.1%}",
            f"- **p50 Latency:** {candidate.p50_latency_ms:.0f}ms | **p90 Latency:** {candidate.p90_latency_ms:.0f}ms",
            f"- **Total Token Cost:** ${candidate.total_cost_usd:.4f}",
        ]

        if brief.trade_offs_summary:
            md.append(f"- **Baseline Delta:** {brief.trade_offs_summary}\n")

        if brief.hard_blockers:
            md.append("### ⚠️ Critical Blockers:")
            for b in brief.hard_blockers:
                md.append(f"- **{b}**")
            md.append("")

        md.append("## 2. Release Gate Assessment")
        md.append("| Gate Name | Status | Threshold | Actual Result | Notes |")
        md.append("|---|---|---|---|---|")
        for g in brief.gates_evaluated:
            badge = "✅ PASS" if g.passed else ("🚫 BLOCKED" if g.is_hard_blocker else "❌ FAIL")
            md.append(f"| {g.gate_name} | {badge} | {g.threshold} | {g.actual_value} | {g.message} |")

        md.append("\n## 3. Failing Cases & Diagnostic Evidence")
        if brief.failing_cases_summary:
            md.append("| Case ID | High Risk? | Diagnostic Root Cause |")
            md.append("|---|---|---|")
            for f in brief.failing_cases_summary:
                risk_tag = "🚨 YES" if f["is_high_risk"] else "No"
                md.append(f"| `{f['case_id']}` | {risk_tag} | {f['diagnostics']} |")
        else:
            md.append("*No test cases failed on this benchmark.*")

        md.append("\n---\n*Generated by AgentEval Studio — The Collaborative Evaluation Workspace for AI Builders.*")
        return "\n".join(md)
