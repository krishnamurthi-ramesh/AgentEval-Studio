# Competitive Teardown: Promptfoo

**Product:** Promptfoo  
**License:** MIT (Open Source)  
**Primary Focus:** CLI & CI/CD evaluation runner for LLMs, prompts, agents, and security red-teaming  
**Source:** [Promptfoo GitHub & Docs](https://www.promptfoo.dev/docs/)

---

## 1. Product Overview & Market Positioning

Promptfoo is one of the most widely adopted open-source test runners for LLM applications and prompts. It follows a declarative, file-based workflow where developers define test suites in a `promptfooconfig.yaml` file and execute them via `npx promptfoo eval`.

### Core Capabilities
- **Declarative YAML Testing:** Test cases define inputs, expected outputs, and assertion types (`equals`, `contains`, `is-json`, `llm-rubric`, `javascript`).
- **Model Matrix Evaluation:** Run the exact same prompt against multiple model providers (OpenAI, Anthropic, Ollama, Bedrock, Vertex AI) side-by-side.
- **Security Red-Teaming:** Automated scanning for prompt injections, jailbreaks, PII leakage, and SSRF vulnerabilities.
- **CI/CD Native:** Runs fast in GitHub Actions and generates pull request comment summaries.

---

## 2. Strengths
- **Low Overhead:** Zero database setup; runs from a single CLI command.
- **Developer-Friendly Ergonomics:** Uses familiar test runner conventions (like Jest or Pytest for LLMs).
- **High Adoption:** Used by teams at OpenAI, Anthropic, and Shopify.

---

## 3. Shortcomings & The Authoring Gap

1. **The "Blank YAML" Problem:** Promptfoo is an **execution runner**, not an **authoring assistant**. The developer must arrive with fully written test cases and assertions. Designing 30 edge cases, adversarial inputs, and tool trajectories manually is painful.
2. **No Test Suite Quality Linting:** Promptfoo will run whatever YAML you provide. It will not warn you if your test suite is overfitted, lacks negative test cases, or has ambiguous assertions.
3. **Agent Trajectory Complexity:** While Promptfoo supports tool calls via custom JavaScript assertions, writing multi-step trajectory assertions in YAML is complex and error-prone.

---

## 4. Strategic Integration with AgentEval Studio

Rather than competing with Promptfoo's battle-tested execution runner, **AgentEval Studio serves as the front-end authoring and linting studio for Promptfoo**:
- **Author:** Use the Behaviour-to-Eval Copilot to design test cases and tool trajectories.
- **Lint:** Use the Eval Quality Linter to catch missing negative cases and safety holes.
- **Export:** Export directly to clean, production-ready `promptfooconfig.yaml`.
- **Run:** Execute with `promptfoo eval`!
