"""
Unit tests for the Eval Quality Linter and Promptfoo Exporter.
"""

from agenteval.linter import EvalQualityLinter
from agenteval.exporters.promptfoo import export_to_promptfoo_yaml
from agenteval.library import load_pack
from agenteval.models import EvalPack, EvalCase, ExpectedToolCall


def test_linter_detects_missing_negative_cases():
    linter = EvalQualityLinter()
    # Pack with ONLY happy path, no negative cases
    defective_pack = EvalPack(
        id="test_defective",
        name="Defective Pack",
        description="Pack with no refusal cases or holdouts",
        category="general",
        cases=[
            EvalCase(
                id="c1",
                category="happy",
                user_input="transfer $100",
                expected_trajectory=[ExpectedToolCall(tool_name="transfer_funds", arguments={"amt": 100})]
            )
        ]
    )

    report = linter.lint(defective_pack)
    assert not report.passed
    assert any(i.rule_id == "LINT-001-NO-NEGATIVE-CASES" for i in report.issues)
    assert any(i.rule_id == "LINT-002-UNGUARDED-HIGH-RISK-TOOL" for i in report.issues)


def test_linter_passes_high_quality_pack():
    linter = EvalQualityLinter()
    banking_pack = load_pack("customer_support_banking")
    report = linter.lint(banking_pack)

    assert report.score >= 80
    assert report.grade in ["A", "B"]


def test_promptfoo_yaml_export():
    banking_pack = load_pack("customer_support_banking")
    yaml_str = export_to_promptfoo_yaml(banking_pack)

    assert "description:" in yaml_str
    assert "providers:" in yaml_str
    assert "tests:" in yaml_str
    assert "get_account_balance" in yaml_str
    assert "transfer_funds" in yaml_str
