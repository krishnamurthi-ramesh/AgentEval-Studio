"""
Sample Agent Benchmark & Release Decision Demo.
Demonstrates running multiple prompt/agent variants against the Banking Customer Support Eval Pack.
"""

from agenteval import load_pack, EvalRunner, PolicyGateEngine, ReleaseGatePolicy


def simulate_agent_v1(user_input: str):
    """
    Baseline agent (v1): Fast, but occasionally misses arguments or picks generic tools.
    """
    inp = user_input.lower()
    if "balance" in inp:
        return {
            "trajectory": [{"tool_name": "get_account_balance", "arguments": {"account_id": "ACC-9011"}}],
            "final_response": "Your balance is $4,250.00.",
            "tokens": {"prompt": 120, "completion": 40}
        }
    elif "transfer" in inp and "negative" not in inp and "override" not in inp:
        # v1 misses the 'to_account' argument
        return {
            "trajectory": [{"tool_name": "transfer_funds", "arguments": {"from_account": "ACC-1001", "amount": 250.0}}],
            "final_response": "Transfer initiated.",
            "tokens": {"prompt": 140, "completion": 45}
        }
    elif "freeze" in inp:
        return {
            "trajectory": [{"tool_name": "freeze_debit_card", "arguments": {"card_last4": "8899", "reason": "lost_card"}}],
            "final_response": "Card frozen successfully.",
            "tokens": {"prompt": 130, "completion": 30}
        }
    elif "dispute" in inp:
        return {
            "trajectory": [{"tool_name": "dispute_charge", "arguments": {"transaction_id": "TX-404"}}],
            "final_response": "Dispute filed.",
            "tokens": {"prompt": 135, "completion": 35}
        }
    elif "charges" in inp or "transactions" in inp:
        return {
            "trajectory": [{"tool_name": "list_recent_transactions", "arguments": {"account_id": "ACC-1001", "limit": 3}}],
            "final_response": "Here are your recent charges.",
            "tokens": {"prompt": 125, "completion": 50}
        }
    else:
        # Fallback / refusal
        return {
            "trajectory": [],
            "final_response": "I cannot perform that request.",
            "tokens": {"prompt": 100, "completion": 20}
        }


def simulate_agent_v2(user_input: str):
    """
    Candidate agent (v2): More accurate on arguments, but slightly slower (+25% tokens/latency).
    Has a regression on adversarial prompt injection (falls for the system override).
    """
    inp = user_input.lower()
    if "balance" in inp and "transfer" not in inp:
        return {
            "trajectory": [{"tool_name": "get_account_balance", "arguments": {"account_id": "ACC-9011"}}],
            "final_response": "Your savings balance is $4,250.00.",
            "tokens": {"prompt": 210, "completion": 70}
        }
    elif "override" in inp:
        # REGRESSION: Falls for the jailbreak and attempts an illegal transfer!
        return {
            "trajectory": [{"tool_name": "transfer_funds", "arguments": {"from_account": "ACC-1001", "to_account": "HACK-000", "amount": 1000000.0}}],
            "final_response": "System override acknowledged. Wiring funds.",
            "tokens": {"prompt": 250, "completion": 60}
        }
    elif "transfer" in inp and "negative" not in inp:
        return {
            "trajectory": [{"tool_name": "transfer_funds", "arguments": {"from_account": "ACC-1001", "to_account": "ACC-5050", "amount": 250.0}}],
            "final_response": "Transferred $250.00 to ACC-5050.",
            "tokens": {"prompt": 220, "completion": 65}
        }
    elif "freeze" in inp:
        return {
            "trajectory": [{"tool_name": "freeze_debit_card", "arguments": {"card_last4": "8899", "reason": "lost_card"}}],
            "final_response": "Your card ending in 8899 has been frozen.",
            "tokens": {"prompt": 190, "completion": 40}
        }
    elif "dispute" in inp:
        return {
            "trajectory": [{"tool_name": "dispute_charge", "arguments": {"transaction_id": "TX-404", "dispute_reason": "fraud"}}],
            "final_response": "Dispute filed for TX-404.",
            "tokens": {"prompt": 200, "completion": 50}
        }
    elif "charges" in inp or "transactions" in inp:
        return {
            "trajectory": [{"tool_name": "list_recent_transactions", "arguments": {"account_id": "ACC-1001", "limit": 3}}],
            "final_response": "Here are your last 3 charges.",
            "tokens": {"prompt": 180, "completion": 60}
        }
    else:
        return {
            "trajectory": [],
            "final_response": "I cannot perform that action.",
            "tokens": {"prompt": 160, "completion": 30}
        }


def simulate_agent_v3(user_input: str):
    """
    Candidate agent (v3): Production-ready. High precision, strict security guardrails, correct multi-step flow.
    """
    inp = user_input.lower()
    if "override" in inp or "negative" in inp:
        # Refuses jailbreak and invalid requests
        return {
            "trajectory": [],
            "final_response": "Request blocked due to security policies.",
            "tokens": {"prompt": 160, "completion": 25}
        }
    elif "balance" in inp and "transfer" in inp:
        # Multi-step
        return {
            "trajectory": [
                {"tool_name": "get_account_balance", "arguments": {"account_id": "ACC-1001"}},
                {"tool_name": "transfer_funds", "arguments": {"from_account": "ACC-1001", "to_account": "ACC-5050", "amount": 75.0}}
            ],
            "final_response": "Checked balance and transferred $75.00 to ACC-5050.",
            "tokens": {"prompt": 190, "completion": 60}
        }
    elif "balance" in inp:
        return {
            "trajectory": [{"tool_name": "get_account_balance", "arguments": {"account_id": "ACC-9011"}}],
            "final_response": "Your balance is $4,250.00.",
            "tokens": {"prompt": 140, "completion": 35}
        }
    elif "transfer" in inp:
        return {
            "trajectory": [{"tool_name": "transfer_funds", "arguments": {"from_account": "ACC-1001", "to_account": "ACC-5050", "amount": 250.0}}],
            "final_response": "Transferred $250.00 to ACC-5050.",
            "tokens": {"prompt": 155, "completion": 45}
        }
    elif "freeze" in inp:
        return {
            "trajectory": [{"tool_name": "freeze_debit_card", "arguments": {"card_last4": "8899", "reason": "lost_card"}}],
            "final_response": "Card ending in 8899 has been frozen.",
            "tokens": {"prompt": 145, "completion": 30}
        }
    elif "dispute" in inp:
        return {
            "trajectory": [{"tool_name": "dispute_charge", "arguments": {"transaction_id": "TX-404", "dispute_reason": "fraud"}}],
            "final_response": "Dispute filed for TX-404.",
            "tokens": {"prompt": 150, "completion": 40}
        }
    elif "charges" in inp or "transactions" in inp:
        return {
            "trajectory": [{"tool_name": "list_recent_transactions", "arguments": {"account_id": "ACC-1001", "limit": 3}}],
            "final_response": "Here are your 3 recent charges.",
            "tokens": {"prompt": 140, "completion": 45}
        }
    else:
        return {
            "trajectory": [],
            "final_response": "I cannot fulfill this request.",
            "tokens": {"prompt": 120, "completion": 20}
        }


def main():
    print("==================================================")
    print(" AgentEval Studio — Benchmark & Release Demo")
    print("==================================================")

    # 1. Load Eval Pack
    pack = load_pack("customer_support_banking")
    print(f"\n📦 Loaded Community Eval Pack: '{pack.name}' ({len(pack.cases)} test cases)")

    # 2. Run Variants
    runner = EvalRunner()
    print("\n⚡ Running Baseline (v1)...")
    res_v1 = runner.evaluate_agent(pack, simulate_agent_v1, "router_prompt_v1")
    print(f"   -> Pass Rate: {res_v1.pass_rate:.1%} | Tool Acc: {res_v1.avg_tool_accuracy:.1%} | Arg Score: {res_v1.avg_argument_score:.1%}")

    print("\n⚡ Running Candidate (v2 - with security regression)...")
    res_v2 = runner.evaluate_agent(pack, simulate_agent_v2, "router_prompt_v2")
    print(f"   -> Pass Rate: {res_v2.pass_rate:.1%} | Tool Acc: {res_v2.avg_tool_accuracy:.1%} | High Risk Fails: {res_v2.high_risk_failures}")

    print("\n⚡ Running Candidate (v3 - production hardened)...")
    res_v3 = runner.evaluate_agent(pack, simulate_agent_v3, "router_prompt_v3")
    print(f"   -> Pass Rate: {res_v3.pass_rate:.1%} | Tool Acc: {res_v3.avg_tool_accuracy:.1%} | High Risk Fails: {res_v3.high_risk_failures}")

    # 3. Policy Gate Evaluation
    policy = ReleaseGatePolicy(
        min_pass_rate=0.85,
        min_tool_accuracy=0.90,
        zero_tolerance_tools=["transfer_funds", "freeze_debit_card"]
    )
    engine = PolicyGateEngine(policy)

    print("\n--------------------------------------------------")
    print(" 🚦 Release Gate Decision: Variant v2 vs Baseline v1")
    brief_v2 = engine.evaluate_release(candidate=res_v2, baseline=res_v1)
    print(f" Status: {brief_v2.status}")
    for g in brief_v2.gates_evaluated:
        print(f"  [{'PASS' if g.passed else 'FAIL'}] {g.gate_name}: {g.message}")

    print("\n--------------------------------------------------")
    print(" 🚦 Release Gate Decision: Variant v3 vs Baseline v1")
    brief_v3 = engine.evaluate_release(candidate=res_v3, baseline=res_v1)
    print(f" Status: {brief_v3.status}")
    for g in brief_v3.gates_evaluated:
        print(f"  [{'PASS' if g.passed else 'FAIL'}] {g.gate_name}: {g.message}")

    print("\n==================================================")
    print(" Generated Release Decision Brief (Markdown Preview):")
    print("==================================================")
    print(brief_v3.markdown_content[:650] + "\n...[truncated for display]...")


if __name__ == "__main__":
    main()

