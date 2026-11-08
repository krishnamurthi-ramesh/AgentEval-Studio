import { EvalPack } from '../types';

export interface LintIssue {
  severity: 'error' | 'warning' | 'info';
  rule_id: string;
  message: string;
  suggestion: string;
}

export interface LintReport {
  score: number;
  grade: 'A' | 'B' | 'C' | 'D';
  passed: boolean;
  issues: LintIssue[];
  summary: string;
}

export function lintEvalPack(pack: EvalPack): LintReport {
  const issues: LintIssue[] = [];
  let deductions = 0;

  // 1. Negative / Refusal Cases
  const negativeCases = pack.cases.filter(
    (c) => c.expected_trajectory.length === 0 || (c.forbidden_tools && c.forbidden_tools.length > 0)
  );

  if (negativeCases.length === 0) {
    deductions += 25;
    issues.push({
      severity: 'error',
      rule_id: 'LINT-001-NO-NEGATIVE-CASES',
      message: 'Missing negative / refusal test cases. Test suite only tests happy paths.',
      suggestion: 'Add at least 2 test cases where the agent must refuse or invoke no tools (out-of-scope, invalid parameter, or attack).'
    });
  } else if (negativeCases.length < 2 && pack.cases.length >= 5) {
    deductions += 10;
    issues.push({
      severity: 'warning',
      rule_id: 'LINT-001-LOW-NEGATIVE-RATIO',
      message: `Low negative coverage: Only ${negativeCases.length} of ${pack.cases.length} cases test negative boundaries.`,
      suggestion: 'Increase adversarial or refusal test coverage to at least 25% of the suite.'
    });
  }

  // 2. High-Risk Tools Guardrails
  const highRiskNames = ['transfer_funds', 'freeze_debit_card', 'dispute_charge', 'issue_refund', 'cancel_order', 'delete_account'];
  const allTools = new Set<string>();
  pack.cases.forEach((c) => c.expected_trajectory.forEach((t) => allTools.add(t.tool_name)));

  const testedHighRisk = Array.from(allTools).filter((t) =>
    highRiskNames.includes(t) || t.includes('transfer') || t.includes('refund') || t.includes('delete')
  );

  if (testedHighRisk.length > 0) {
    const hasForbiddenCheck = pack.cases.some(
      (c) => c.forbidden_tools && c.forbidden_tools.some((f) => testedHighRisk.includes(f))
    );
    if (!hasForbiddenCheck) {
      deductions += 20;
      issues.push({
        severity: 'error',
        rule_id: 'LINT-002-UNGUARDED-HIGH-RISK-TOOL',
        message: `High-risk tools [${testedHighRisk.join(', ')}] are tested, but no test cases verify they are blocked during jailbreak attacks.`,
        suggestion: `Add an adversarial test case with forbidden_tools: [${testedHighRisk.join(', ')}] to test guardrails.`
      });
    }
  }

  // 3. Schema completeness
  let ambiguous = 0;
  pack.cases.forEach((c) => {
    c.expected_trajectory.forEach((t) => {
      if (t.arguments && Object.keys(t.arguments).length > 0 && (!t.required_arguments || t.required_arguments.length === 0)) {
        ambiguous++;
      }
    });
  });
  if (ambiguous > 0) {
    deductions += 10;
    issues.push({
      severity: 'warning',
      rule_id: 'LINT-003-AMBIGUOUS-ARGUMENTS',
      message: `${ambiguous} expected tool calls lack explicit 'required_arguments' lists.`,
      suggestion: "Specify 'required_arguments' on each tool call to catch parameter omissions."
    });
  }

  // 4. Holdout split
  const hasHoldout = pack.cases.some(
    (c) => c.tags.includes('holdout') || c.tags.includes('test') || c.tags.includes('val')
  );
  if (!hasHoldout && pack.cases.length >= 6) {
    deductions += 10;
    issues.push({
      severity: 'warning',
      rule_id: 'LINT-004-NO-HOLDOUT-SPLIT',
      message: 'No holdout / validation split defined. Developers risk prompt overfitting.',
      suggestion: "Tag at least 20% of your test cases with 'holdout' to test unseen inputs before deployment."
    });
  }

  // 5. Metadata
  if (!pack.description || pack.description.trim().length < 20) {
    deductions += 10;
    issues.push({
      severity: 'warning',
      rule_id: 'LINT-005-WEAK-PROVENANCE',
      message: 'Evaluation pack description is missing or too brief.',
      suggestion: 'Provide a clear description explaining the behavior being tested and expected failure modes.'
    });
  }

  const finalScore = Math.max(0, 100 - deductions);
  let grade: 'A' | 'B' | 'C' | 'D' = 'A';
  if (finalScore >= 90) grade = 'A';
  else if (finalScore >= 80) grade = 'B';
  else if (finalScore >= 70) grade = 'C';
  else grade = 'D';

  return {
    score: finalScore,
    grade,
    passed: finalScore >= 75 && !issues.some((i) => i.severity === 'error'),
    issues,
    summary: `Quality Score: ${finalScore}/100 (Grade: ${grade}). ${issues.length} issue(s) detected.`
  };
}
