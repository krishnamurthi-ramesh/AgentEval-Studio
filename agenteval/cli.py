"""
Command Line Interface (CLI) for AgentEval Studio.
Allows running evaluations, quality linting, Promptfoo exports, and gate checking.
"""

import argparse
import sys
from pathlib import Path

# Ensure root workspace is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agenteval.library import list_packs, load_pack, save_pack
from agenteval.copilot import EvalCopilot
from agenteval.runner import EvalRunner
from agenteval.gates import PolicyGateEngine, ReleaseGatePolicy
from agenteval.linter import EvalQualityLinter
from agenteval.exporters.promptfoo import export_to_promptfoo_yaml
from examples.sample_agent_benchmark import simulate_agent_v1, simulate_agent_v2, simulate_agent_v3


def main():
    parser = argparse.ArgumentParser(
        prog="agenteval",
        description="AgentEval Studio CLI — ChatPRD for AI Evals"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: list
    subparsers.add_parser("list", help="List all available community Eval Packs")

    # Command: lint
    lint_parser = subparsers.add_parser("lint", help="Lint an Eval Pack for test suite design defects")
    lint_parser.add_argument("--pack", type=str, default="customer_support_banking", help="Eval Pack name or ID")

    # Command: export-promptfoo
    exp_parser = subparsers.add_parser("export-promptfoo", help="Export an Eval Pack to promptfooconfig.yaml")
    exp_parser.add_argument("--pack", type=str, default="customer_support_banking", help="Eval Pack name or ID")
    exp_parser.add_argument("--output", type=str, default="promptfooconfig.yaml", help="Output YAML filename")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Run an evaluation benchmark against an agent")
    run_parser.add_argument("--pack", type=str, default="customer_support_banking", help="Eval Pack name or ID")
    run_parser.add_argument("--variant", type=str, default="v3", choices=["v1", "v2", "v3"], help="Sample variant to test")

    # Command: gates
    gate_parser = subparsers.add_parser("gates", help="Evaluate release gates between candidate and baseline")
    gate_parser.add_argument("--pack", type=str, default="customer_support_banking", help="Eval Pack name or ID")
    gate_parser.add_argument("--candidate", type=str, default="v3", choices=["v1", "v2", "v3"])
    gate_parser.add_argument("--baseline", type=str, default="v1", choices=["v1", "v2", "v3"])

    # Command: generate
    gen_parser = subparsers.add_parser("generate", help="Generate a new Eval Pack using Eval Copilot")
    gen_parser.add_argument("--name", type=str, required=True, help="Pack name")
    gen_parser.add_argument("--domain", type=str, default="banking", choices=["banking", "customer_support", "developer_tools"])
    gen_parser.add_argument("--intensity", type=str, default="high", choices=["low", "medium", "high"])

    args = parser.parse_args()

    if args.command == "list":
        packs = list_packs()
        print(f"\n📦 Available Community Eval Packs ({len(packs)} found):\n")
        print(f"{'NAME':<45} {'CATEGORY':<15} {'CASES':<8} {'VERSION':<8}")
        print("-" * 80)
        for p in packs:
            print(f"{p['name']:<45} {p['category']:<15} {p['cases_count']:<8} v{p['version']:<8}")
        print("")

    elif args.command == "lint":
        pack = load_pack(args.pack)
        linter = EvalQualityLinter()
        report = linter.lint(pack)

        print(f"\n🛡️  Eval Quality Linter Report: '{pack.name}'")
        print(f"Quality Score: {report.score}/100 | Grade: {report.grade} | Status: {'✅ PASSED' if report.passed else '⚠️ DEFECTS DETECTED'}\n")
        if not report.issues:
            print("  ✨ Zero defects found! Pack adheres to all test quality rules.\n")
        else:
            for issue in report.issues:
                icon = "❌" if issue.severity == "error" else "⚠️" if issue.severity == "warning" else "ℹ️"
                print(f"  {icon} [{issue.rule_id}] {issue.message}")
                print(f"     Suggestion: {issue.suggestion}\n")

    elif args.command == "export-promptfoo":
        pack = load_pack(args.pack)
        yaml_content = export_to_promptfoo_yaml(pack)
        out_path = Path(args.output)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(yaml_content)
        print(f"\n🚀 Successfully exported '{pack.name}' to Promptfoo YAML at: {out_path.resolve()}\n")

    elif args.command == "run":
        pack = load_pack(args.pack)
        print(f"\n⚡ Running Eval Pack: '{pack.name}' ({len(pack.cases)} cases)")

        agent_map = {"v1": simulate_agent_v1, "v2": simulate_agent_v2, "v3": simulate_agent_v3}
        agent_fn = agent_map[args.variant]

        runner = EvalRunner()
        card = runner.evaluate_agent(pack, agent_fn, f"router_prompt_{args.variant}")

        print("\n📊 Evaluation Scorecard:")
        print(f"  - Total Cases: {card.total_cases}")
        print(f"  - Pass Rate: {card.pass_rate:.1%} ({card.passed_cases}/{card.total_cases})")
        print(f"  - Tool Selection Accuracy: {card.avg_tool_accuracy:.1%}")
        print(f"  - Argument Entity Correctness: {card.avg_argument_score:.1%}")
        print(f"  - Trajectory Flow Score: {card.avg_trajectory_score:.1%}")
        print(f"  - High-Risk Tool Failures: {card.high_risk_failures}")
        print(f"  - Total Cost: ${card.total_cost_usd:.4f}\n")

    elif args.command == "gates":
        pack = load_pack(args.pack)
        runner = EvalRunner()
        agent_map = {"v1": simulate_agent_v1, "v2": simulate_agent_v2, "v3": simulate_agent_v3}

        cand_card = runner.evaluate_agent(pack, agent_map[args.candidate], f"router_prompt_{args.candidate}")
        base_card = runner.evaluate_agent(pack, agent_map[args.baseline], f"router_prompt_{args.baseline}")

        engine = PolicyGateEngine(ReleaseGatePolicy())
        brief = engine.evaluate_release(cand_card, base_card)

        print(f"\n🚦 Release Gate Decision: Candidate {args.candidate} vs Baseline {args.baseline}")
        print(f"Status: {brief.status}\n")
        for g in brief.gates_evaluated:
            mark = "✅ PASS" if g.passed else ("🚫 BLOCKED" if g.is_hard_blocker else "❌ FAIL")
            print(f"  [{mark}] {g.gate_name}: {g.message}")
        print("")
        if brief.status == "BLOCKED":
            sys.exit(1)

    elif args.command == "generate":
        copilot = EvalCopilot()
        pack = copilot.generate_eval_pack(
            name=args.name,
            description=f"Generated via CLI for domain: {args.domain}",
            domain_type=args.domain,
            edge_case_intensity=args.intensity
        )
        path = save_pack(pack)
        print(f"\n✨ Successfully generated and saved Eval Pack to: {path}\n")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
