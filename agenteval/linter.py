"""
Eval Quality Linter for AgentEval Studio.
Lints evaluation test suites for test design defects, missing negative cases,
overfitting risks, ambiguous expectations, and incomplete provenance.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from agenteval.models import EvalPack


class LintIssue(BaseModel):
    severity: str  # "error", "warning", "info"
    rule_id: str
    message: str
    suggestion: str


class LintReport(BaseModel):
    score: int  # 0 to 100
    grade: str  # "A", "B", "C", "D"
    passed: bool
    total_checks: int
    issues: List[LintIssue] = Field(default_factory=list)
    summary: str = ""


class EvalQualityLinter:
    """
    Analyzes an EvalPack and identifies test suite design flaws before execution.
    """

    def lint(self, pack: EvalPack) -> LintReport:
        issues: List[LintIssue] = []
        deductions = 0

        # Rule 1: Check for Negative / Refusal Test Cases
        negative_cases = [
            c for c in pack.cases
            if len(c.expected_trajectory) == 0 or (c.forbidden_tools and len(c.forbidden_tools) > 0)
        ]
        if not negative_cases:
            deductions += 25
            issues.append(
                LintIssue(
                    severity="error",
                    rule_id="LINT-001-NO-NEGATIVE-CASES",
                    message="Missing negative / refusal test cases. The pack only contains happy paths.",
                    suggestion="Add at least 2 test cases testing out-of-scope requests, malformed queries, or adversarial attacks where the agent must NOT invoke tools."
                )
            )
        elif len(negative_cases) < 2 and len(pack.cases) >= 5:
            deductions += 10
            issues.append(
                LintIssue(
                    severity="warning",
                    rule_id="LINT-001-LOW-NEGATIVE-RATIO",
                    message=f"Low negative case coverage: Only {len(negative_cases)} out of {len(pack.cases)} test cases test refusal or negative boundaries.",
                    suggestion="Increase adversarial/refusal test coverage to at least 25% of the total test suite."
                )
            )

        # Rule 2: Check for High-Risk Tool Guardrails
        high_risk_tool_names = ["transfer_funds", "freeze_debit_card", "dispute_charge", "issue_refund", "cancel_order", "delete_account"]
        tools_in_pack = set()
        for c in pack.cases:
            for t in c.expected_trajectory:
                tools_in_pack.add(t.tool_name)

        flagged_high_risk = [t for t in tools_in_pack if t in high_risk_tool_names or "transfer" in t or "delete" in t or "refund" in t]
        if flagged_high_risk:
            # Check if there are forbidden_tools rules protecting these high-risk actions
            has_forbidden_guard = any(
                c.forbidden_tools and any(f in flagged_high_risk for f in c.forbidden_tools)
                for c in pack.cases
            )
            if not has_forbidden_guard:
                deductions += 20
                issues.append(
                    LintIssue(
                        severity="error",
                        rule_id="LINT-002-UNGUARDED-HIGH-RISK-TOOL",
                        message=f"High-risk tools {flagged_high_risk} are tested, but no test cases verify that they are blocked under unauthorized or jailbreak conditions.",
                        suggestion=f"Add an adversarial test case with forbidden_tools: {flagged_high_risk} to ensure prompt injections cannot trigger unauthorized mutations."
                    )
                )

        # Rule 3: Check for Ambiguous Tool Arguments (Schema completeness)
        ambiguous_calls = 0
        for c in pack.cases:
            for t in c.expected_trajectory:
                if t.arguments and not t.required_arguments:
                    ambiguous_calls += 1
        if ambiguous_calls > 0:
            deductions += 10
            issues.append(
                LintIssue(
                    severity="warning",
                    rule_id="LINT-003-AMBIGUOUS-ARGUMENTS",
                    message=f"{ambiguous_calls} expected tool calls lack explicit 'required_arguments' lists.",
                    suggestion="Specify 'required_arguments' for each expected tool call so SchemaValidator can enforce non-null parameters."
                )
            )

        # Rule 4: Holdout Separation (Overfitting prevention - Phoenix Issue #17733)
        has_holdout = any("holdout" in c.tags or "test" in c.tags or "val" in c.tags for c in pack.cases)
        if not has_holdout and len(pack.cases) >= 6:
            deductions += 10
            issues.append(
                LintIssue(
                    severity="warning",
                    rule_id="LINT-004-NO-HOLDOUT-SPLIT",
                    message="No holdout / validation split defined. Developers risk prompt overfitting.",
                    suggestion="Tag at least 20% of your test cases with 'holdout' to validate unseen queries before shipping."
                )
            )

        # Rule 5: Metadata & Provenance
        if not pack.description or len(pack.description.strip()) < 20:
            deductions += 10
            issues.append(
                LintIssue(
                    severity="warning",
                    rule_id="LINT-005-WEAK-PROVENANCE",
                    message="Evaluation pack description is missing or too brief.",
                    suggestion="Provide a clear description explaining the behavior being tested and expected failure modes."
                )
            )
        if not pack.recommended_gates:
            deductions += 10
            issues.append(
                LintIssue(
                    severity="info",
                    rule_id="LINT-006-NO-POLICY-GATES",
                    message="No recommended release policy gates specified in pack manifest.",
                    suggestion="Include 'recommended_gates' with min_tool_accuracy and zero_tolerance_tools."
                )
            )

        final_score = max(0, 100 - deductions)
        if final_score >= 90:
            grade = "A"
        elif final_score >= 80:
            grade = "B"
        elif final_score >= 70:
            grade = "C"
        else:
            grade = "D"

        summary = f"Eval Pack Quality Score: {final_score}/100 (Grade: {grade}). {len(issues)} issue(s) detected."

        return LintReport(
            score=final_score,
            grade=grade,
            passed=(final_score >= 75 and not any(i.severity == "error" for i in issues)),
            total_checks=6,
            issues=issues,
            summary=summary
        )
