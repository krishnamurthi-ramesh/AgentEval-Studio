# Quickstart Guide — AgentEval Studio

Get up and running with AgentEval Studio in under 5 minutes.

---

## 1. Option A: Modern Web Application (Recommended)

The web workbench provides an interactive, visual interface for generating evaluation packs with the Copilot, browsing the community library, comparing agent runs, and inspecting release gates.

```bash
# Clone the repository
git clone https://github.com/krishnamurthi-ramesh/AgentEval-Studio.git
cd AgentEval-Studio/frontend

# Install dependencies and start local dev server
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 2. Option B: Python SDK & CLI Runner

For developers running benchmarks in terminal or automated CI/CD pipelines.

### Installation
```bash
cd AgentEval-Studio
pip install -e .
```

### CLI Commands

```bash
# List all community packs
agenteval list

# Run evaluation on a sample agent variant (v1, v2, or v3)
agenteval run --pack customer_support_banking --variant v3

# Evaluate release policy gates
agenteval gates --pack customer_support_banking --candidate v3 --baseline v1

# Generate a new Eval Pack with Eval Copilot
agenteval generate --name "Order Management Assistant" --domain customer_support --intensity high
```

---

## 3. Option C: Using in Your Own Python Code

```python
from agenteval import load_pack, EvalRunner, PolicyGateEngine, ReleaseGatePolicy

# 1. Load an Eval Pack
pack = load_pack("customer_support_banking")

# 2. Define your agent function
def my_agent(user_prompt: str):
    # Your agent invocation logic here
    return {
        "trajectory": [
            {"tool_name": "get_account_balance", "arguments": {"account_id": "ACC-9011"}}
        ],
        "final_response": "Your balance is $4,250.00."
    }

# 3. Evaluate agent
runner = EvalRunner()
candidate_card = runner.evaluate_agent(pack, my_agent, "my_agent_v1")

# 4. Check Release Gates
policy = ReleaseGatePolicy(min_tool_accuracy=0.90, max_latency_regression_pct=15.0)
engine = PolicyGateEngine(policy)
brief = engine.evaluate_release(candidate_card)

print(f"Status: {brief.status}")
print(brief.markdown_content)
```

