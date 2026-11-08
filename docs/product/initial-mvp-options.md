# Initial MVP Options & Scoping Hypotheses

## Objective
Evaluate potential MVP wedges for AgentEval Studio that provide immediate developer utility while demonstrating crisp AI PM scoping.

---

### Option A: The "Release Gate & Decision Brief" Workbench (Recommended Direction)
- **Concept:** A local-first evaluation workbench specifically for tool-using agents that executes candidate prompts/models against a benchmark dataset, evaluates tool selection, argument accuracy, trajectory, and cost/latency, and checks them against user-defined **Release Criteria Gates** to generate an automated **Release Decision Brief**.
- **Target Persona:** Applied AI Engineer / AI Product Manager collaborating on shipping agent updates.
- **Why it wins:**
  - Solves the exact gap between "we ran evals" and "can we deploy this?"
  - Differentiates from raw observability platforms (Phoenix/LangSmith) by being opinionated about decision-making.
  - Zero cloud setup needed; runs locally via CLI or Streamlit UI.

---

### Option B: Trajectory & Tool-Call Debugger
- **Concept:** A visual diffing tool for agent execution paths. Focuses purely on comparing the step-by-step tool trajectories between two agent runs (e.g., Run A took 3 steps with Tool X, Run B took 7 steps with Tool Y and circled in a loop).
- **Target Persona:** AI Agent Developer debugging multi-agent orchestration.
- **Risk:** High overlap with Phoenix and LangSmith trace viewers; lacks the high-level release decision aspect that AI PMs care about.

---

### Option C: Standalone Agent Evaluators Library
- **Concept:** A pure headless Python package offering deterministic evaluators for tool calling (tool selection precision/recall, JSON schema validity, argument entity accuracy, trajectory edit distance).
- **Target Persona:** Backend AI engineers writing CI/CD tests.
- **Risk:** Lower visual impact for demonstrations; doesn't solve the stakeholder trade-off and release-decision workflow.

---

## Strategic Recommendation
Build **Option A**, powered under the hood by the deterministic evaluators of **Option C**. This provides an extensible Python SDK for developers and CI/CD, plus an intuitive local UI workbench that turns evaluation data into transparent release decisions.
