"""
Unit tests for the Eval Copilot and Pack Library.
"""

from agenteval.copilot import EvalCopilot
from agenteval.library import list_packs, load_pack


def test_eval_copilot_generation():
    copilot = EvalCopilot()
    pack = copilot.generate_eval_pack(
        name="Crypto Wallet Support",
        description="Assists users with checking balances, sending tokens, and staking assets.",
        domain_type="banking",
        edge_case_intensity="high"
    )

    assert pack.name == "Crypto Wallet Support"
    assert len(pack.cases) >= 6
    assert any("adversarial" in c.category for c in pack.cases)
    assert len(pack.rubrics) > 0


def test_library_packs():
    packs = list_packs()
    assert len(packs) >= 3
    pack_names = [p["name"] for p in packs]
    assert any("Banking" in name for name in pack_names)

    # Test loading
    banking_pack = load_pack("customer_support_banking")
    assert len(banking_pack.cases) > 0
    assert banking_pack.category == "finance"

