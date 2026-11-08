"""
Command Line Interface (CLI) for AgentEval Studio.
Allows running evaluations, listing packs, and evaluating release gates in terminal and CI/CD.
"""

import argparse
import sys
import json
import importlib
from pathlib import Path

from agenteval.library import list_packs, load_pack, save_pack
from agenteval.copilot import EvalCopilot
from agenteval.runner import EvalRunner
from agenteval.gates import PolicyGateEngine, ReleaseGatePolicy
from examples.sample_agent_benchmark import simulate_agent_v1, simulate_agent_v2, simulate_agent_v3


def main():
    parser = argparse.ArgumentParser(
        prog="agenteval",
        description="AgentEval Studio CLI — ChatPRD for AI Evals"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: list
    list_parser = subparsers.add_parser("list", help="List all available community Eval Packs")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Run an evaluation benchmark against an agent")
    run_parser.add_argument("--pack", type=str, default="customer_support_banking", help="Eval Pack name or ID")
    run_parser.add_argument("--variant", type=str, default="v3", choices=["v1", "v2", "v3"], help="Sample variant to test (v1/v2/v3)")

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

    # Command: ui
    ui_parser = subparsers.add_parser("ui", help="Launch the interactive Streamlit Workbench")

    args = parser.parse_args()

    if args.command == "list":
        packs = list_packs()
        print(f"\n📦 Available Community Eval Packs ({len(packs)} found):\n")
        print(f"{'NAME':<45} {'CATEGORY':<15} {'CASES':<8} {'VERSION':<8}")
        print("-" * 80)
        for p in packs:
            print(f"{p['name']:<45} {p['category']:<15} {p['cases_count']:<8} v{p['version']:<8}")
        print("")

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

    elif args.command == "ui":
        import subprocess
        app_path = Path(__file__).parent / "app.py"
        subprocess.run(["streamlit", "run", str(app_path)])

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
