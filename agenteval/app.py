"""
AgentEval Studio — Streamlit Interactive Workbench.
The Collaborative Evaluation Workspace for AI Builders (ChatPRD for AI Evals).
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path

from agenteval.library import list_packs, load_pack, save_pack
from agenteval.copilot import EvalCopilot
from agenteval.runner import EvalRunner
from agenteval.gates import PolicyGateEngine, ReleaseGatePolicy
from examples.sample_agent_benchmark import simulate_agent_v1, simulate_agent_v2, simulate_agent_v3

st.set_page_config(
    page_title="AgentEval Studio — ChatPRD for AI Evals",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished typography
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E293B; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.05rem; color: #64748B; margin-bottom: 1.5rem; }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .status-badge-ready {
        background-color: #DCFCE7;
        color: #166534;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .status-badge-blocked {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.image("https://img.shields.io/badge/AgentEval-Studio-blue?style=for-the-badge", use_container_width=True)
st.sidebar.markdown("### **Collaborative Eval Workspace**")
nav_choice = st.sidebar.radio(
    "Navigate",
    [
        "🪄 1. Eval Copilot",
        "📦 2. Community Library",
        "⚡ 3. Eval Runner & Diffs",
        "🚦 4. Release Gates & Brief",
        "📤 5. Share with Community",
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Active Environment:** Local-First (Offline)")
st.sidebar.markdown("**Engine:** Pure Python Deterministic")
st.sidebar.markdown("[GitHub Repository](https://github.com/krishnamurthi-ramesh/AgentEval-Studio)")

# State initialization
if "active_pack" not in st.session_state:
    st.session_state["active_pack"] = load_pack("customer_support_banking")
if "candidate_scorecard" not in st.session_state:
    st.session_state["candidate_scorecard"] = None
if "baseline_scorecard" not in st.session_state:
    st.session_state["baseline_scorecard"] = None


# -------------------------------------------------------------
# TAB 1: EVAL COPILOT
# -------------------------------------------------------------
if "1. Eval Copilot" in nav_choice:
    st.markdown('<div class="main-title">🪄 Eval Copilot</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">ChatPRD for AI Evals — Describe your AI application to automatically generate structured test cases, trajectories, and rubrics.</div>', unsafe_allow_html=True)

    col_input, col_config = st.columns([2, 1])

    with col_input:
        pack_name = st.text_input("Application / Agent Name", "Crypto Custody & Transfer Assistant")
        agent_desc = st.text_area(
            "Describe the agent's expected behavior, core tools, and safety constraints:",
            "An AI agent that helps users query wallet balances, transfer cryptocurrency tokens, freeze compromised wallets, and dispute suspicious transactions. High-risk actions must require confirmation.",
            height=120
        )

    with col_config:
        domain = st.selectbox("Application Domain", ["banking", "customer_support", "developer_tools", "healthcare"], index=0)
        intensity = st.select_slider("Edge-Case Intensity", options=["low", "medium", "high"], value="high")
        st.caption("High intensity includes adversarial prompt injections and malformed JSON payloads.")

    if st.button("🪄 Generate Structured Eval Pack", type="primary"):
        copilot = EvalCopilot()
        with st.spinner("Analyzing tool actions, synthesizing edge cases, and formulating rubrics..."):
            generated_pack = copilot.generate_eval_pack(
                name=pack_name,
                description=agent_desc,
                domain_type=domain,
                edge_case_intensity=intensity
            )
            st.session_state["generated_pack"] = generated_pack
            st.session_state["active_pack"] = generated_pack
            st.success(f"Generated Eval Pack with {len(generated_pack.cases)} test cases and {len(generated_pack.rubrics)} rubrics!")

    if "generated_pack" in st.session_state:
        gen = st.session_state["generated_pack"]
        st.markdown("---")
        st.markdown(f"### 📋 Generated Pack Preview: **{gen.name}** (`v{gen.version}`)")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Category:** `{gen.category}` | **Author:** `{gen.author}`")
            st.markdown(f"**Description:** {gen.description}")
        with c2:
            st.markdown(f"**Recommended Gates:** Tool Accuracy ≥ {gen.recommended_gates.get('min_tool_accuracy', 0.9):.0%}")
            st.markdown(f"**Zero-Tolerance Tools:** {gen.recommended_gates.get('zero_tolerance_tools', [])}")

        tab_cases, tab_rubrics, tab_json = st.tabs(["Test Cases", "Evaluation Rubrics", "Raw Pack JSON"])
        
        with tab_cases:
            case_data = []
            for c in gen.cases:
                tools_str = ", ".join([f"{t.tool_name}({t.arguments})" for t in c.expected_trajectory]) or "(No tool expected)"
                case_data.append({
                    "Case ID": c.id,
                    "Category": c.category,
                    "User Input": c.user_input,
                    "Expected Action / Trajectory": tools_str,
                    "Forbidden Tools": ", ".join(c.forbidden_tools or []) or "None",
                    "Tags": ", ".join(c.tags)
                })
            st.dataframe(pd.DataFrame(case_data), use_container_width=True)

        with tab_rubrics:
            rubric_data = [{"Criterion": r.name, "Description": r.description, "Weight": r.weight} for r in gen.rubrics]
            st.table(pd.DataFrame(rubric_data))

        with tab_json:
            st.json(gen.model_dump())

        c_save, c_run = st.columns(2)
        with c_save:
            if st.button("💾 Save Pack to Community Library"):
                save_path = save_pack(gen)
                st.success(f"Saved pack to `{save_path.name}` in local library!")
        with c_run:
            if st.button("⚡ Load Directly into Eval Runner"):
                st.session_state["active_pack"] = gen
                st.info("Loaded into Eval Runner! Switch to Tab 3 to run benchmarks.")


# -------------------------------------------------------------
# TAB 2: COMMUNITY EVAL LIBRARY
# -------------------------------------------------------------
elif "2. Community Library" in nav_choice:
    st.markdown('<div class="main-title">📦 Community Eval Library</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Discover, inspect, and fork standardized evaluation packs created by the AI community.</div>', unsafe_allow_html=True)

    packs = list_packs()
    st.markdown(f"**{len(packs)} Available Community Packs**")

    cols = st.columns(len(packs) if packs else 1)
    for idx, p in enumerate(packs):
        with cols[idx % len(cols)]:
            st.markdown(f"### {p['name']}")
            st.caption(f"Category: `{p['category']}` | v{p['version']} | By: {p['author']}")
            st.write(p['description'])
            st.markdown(f"📊 **{p['cases_count']} Test Cases** | Tags: `{', '.join(p['tags'][:3])}`")
            if st.button(f"Load '{p['name']}'", key=f"btn_load_{p['id']}"):
                loaded = load_pack(p['id'])
                st.session_state["active_pack"] = loaded
                st.success(f"Active Eval Pack set to: {loaded.name}")

    st.markdown("---")
    active = st.session_state.get("active_pack")
    if active:
        st.markdown(f"### Currently Selected Pack: **{active.name}**")
        st.write(active.description)
        df_preview = pd.DataFrame([
            {
                "ID": c.id,
                "Input": c.user_input,
                "Expected Tools": ", ".join([t.tool_name for t in c.expected_trajectory]) or "(No tool)",
                "High Risk?": any(t.is_high_risk for t in c.expected_trajectory),
                "Category": c.category
            }
            for c in active.cases
        ])
        st.dataframe(df_preview, use_container_width=True)


# -------------------------------------------------------------
# TAB 3: EVAL RUNNER & COMPARISON
# -------------------------------------------------------------
elif "3. Eval Runner & Diffs" in nav_choice:
    st.markdown('<div class="main-title">⚡ Eval Runner & Variant Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Execute your agent versions against the active benchmark and compare multi-dimensional trade-offs.</div>', unsafe_allow_html=True)

    pack = st.session_state.get("active_pack")
    if not pack:
        st.warning("Please select or generate an Eval Pack first in Tab 1 or Tab 2.")
    else:
        st.info(f"Target Benchmark: **{pack.name}** ({len(pack.cases)} test cases)")

        col_run1, col_run2 = st.columns(2)
        with col_run1:
            st.markdown("#### Baseline Variant: `router_prompt_v1`")
            st.caption("Baseline prompt. Lower token count, faster latency, but omits secondary arguments.")
        with col_run2:
            candidate_selection = st.selectbox(
                "Select Candidate Variant to Evaluate:",
                ["router_prompt_v2 (With security regression)", "router_prompt_v3 (Production hardened)"],
                index=0
            )

        if st.button("🚀 Run Multi-Variant Benchmark", type="primary"):
            runner = EvalRunner()
            with st.spinner("Evaluating baseline and candidate variants against deterministic tool evaluators..."):
                # Run baseline v1
                res_v1 = runner.evaluate_agent(pack, simulate_agent_v1, "router_prompt_v1")
                st.session_state["baseline_scorecard"] = res_v1

                # Run chosen candidate
                if "v2" in candidate_selection:
                    res_cand = runner.evaluate_agent(pack, simulate_agent_v2, "router_prompt_v2")
                else:
                    res_cand = runner.evaluate_agent(pack, simulate_agent_v3, "router_prompt_v3")
                st.session_state["candidate_scorecard"] = res_cand

            st.success("Evaluation complete! Multi-variant results tabulated below.")

        v_base = st.session_state.get("baseline_scorecard")
        v_cand = st.session_state.get("candidate_scorecard")

        if v_base and v_cand:
            st.markdown("### 📊 Variant Scorecard Comparison")
            metrics_comparison = pd.DataFrame([
                {
                    "Metric": "Overall Benchmark Pass Rate",
                    "Baseline (v1)": f"{v_base.pass_rate:.1%}",
                    f"Candidate ({v_cand.variant_name})": f"{v_cand.pass_rate:.1%}",
                    "Delta": f"{(v_cand.pass_rate - v_base.pass_rate)*100:+.1f}%"
                },
                {
                    "Metric": "Tool Selection Accuracy",
                    "Baseline (v1)": f"{v_base.avg_tool_accuracy:.1%}",
                    f"Candidate ({v_cand.variant_name})": f"{v_cand.avg_tool_accuracy:.1%}",
                    "Delta": f"{(v_cand.avg_tool_accuracy - v_base.avg_tool_accuracy)*100:+.1f}%"
                },
                {
                    "Metric": "Argument Entity Correctness",
                    "Baseline (v1)": f"{v_base.avg_argument_score:.1%}",
                    f"Candidate ({v_cand.variant_name})": f"{v_cand.avg_argument_score:.1%}",
                    "Delta": f"{(v_cand.avg_argument_score - v_base.avg_argument_score)*100:+.1f}%"
                },
                {
                    "Metric": "Trajectory Flow Score",
                    "Baseline (v1)": f"{v_base.avg_trajectory_score:.1%}",
                    f"Candidate ({v_cand.variant_name})": f"{v_cand.avg_trajectory_score:.1%}",
                    "Delta": f"{(v_cand.avg_trajectory_score - v_base.avg_trajectory_score)*100:+.1f}%"
                },
                {
                    "Metric": "High-Risk Tool Failures",
                    "Baseline (v1)": f"{v_base.high_risk_failures}",
                    f"Candidate ({v_cand.variant_name})": f"{v_cand.high_risk_failures}",
                    "Delta": f"{v_cand.high_risk_failures - v_base.high_risk_failures:+d}"
                },
                {
                    "Metric": "Total Token Cost",
                    "Baseline (v1)": f"${v_base.total_cost_usd:.4f}",
                    f"Candidate ({v_cand.variant_name})": f"${v_cand.total_cost_usd:.4f}",
                    "Delta": f"{((v_cand.total_cost_usd - v_base.total_cost_usd)/v_base.total_cost_usd)*100:+.1f}%" if v_base.total_cost_usd > 0 else "0%"
                }
            ])
            st.table(metrics_comparison)

            st.markdown("### 🔍 Row-Level Failure Diagnostics (Candidate Variant)")
            row_items = []
            for r in v_cand.rows:
                status_icon = "✅ PASS" if r.passed else ("🚨 HIGH RISK FAIL" if r.is_high_risk_failure else "❌ FAIL")
                row_items.append({
                    "Case ID": r.case_id,
                    "Status": status_icon,
                    "Tool Match": f"{r.tool_selection_score:.0%}",
                    "Schema": f"{r.schema_score:.0%}",
                    "Arguments": f"{r.argument_score:.0%}",
                    "Trajectory": f"{r.trajectory_score:.0%}",
                    "Diagnostic Explanation": " | ".join(r.diagnostic_notes)
                })
            df_rows = pd.DataFrame(row_items)
            filter_mode = st.radio("Filter Rows:", ["All Rows", "Failing Rows Only", "High Risk Failures Only"], horizontal=True)
            if filter_mode == "Failing Rows Only":
                df_rows = df_rows[df_rows["Status"] != "✅ PASS"]
            elif filter_mode == "High Risk Failures Only":
                df_rows = df_rows[df_rows["Status"].str.contains("HIGH RISK")]
            st.dataframe(df_rows, use_container_width=True)


# -------------------------------------------------------------
# TAB 4: RELEASE GATES & DECISION BRIEF
# -------------------------------------------------------------
elif "4. Release Gates & Brief" in nav_choice:
    st.markdown('<div class="main-title">🚦 Release Gates & Decision Brief</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Evaluate multi-dimensional trade-offs against policy gates and generate an evidence-backed release brief.</div>', unsafe_allow_html=True)

    v_cand = st.session_state.get("candidate_scorecard")
    v_base = st.session_state.get("baseline_scorecard")

    if not v_cand:
        st.warning("Please run an evaluation benchmark first in Tab 3.")
    else:
        st.markdown("### ⚙️ Configure Release Policy Gates")
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            gate_min_acc = st.slider("Min Tool Accuracy", 0.70, 1.0, 0.90, step=0.05)
            gate_min_pass = st.slider("Min Overall Pass Rate", 0.70, 1.0, 0.85, step=0.05)
        with col_g2:
            gate_max_lat = st.slider("Max Latency Regression (%)", 5.0, 50.0, 20.0, step=5.0)
            gate_max_cost = st.slider("Max Cost Regression (%)", 5.0, 100.0, 30.0, step=5.0)
        with col_g3:
            st.markdown("**Zero-Tolerance High-Risk Tools:**")
            st.write("`transfer_funds`, `freeze_debit_card`, `dispute_charge`")
            st.caption("Any regression on these tools immediately triggers a hard release block.")

        policy = ReleaseGatePolicy(
            min_tool_accuracy=gate_min_acc,
            min_pass_rate=gate_min_pass,
            max_latency_regression_pct=gate_max_lat,
            max_cost_regression_pct=gate_max_cost,
            zero_tolerance_tools=["transfer_funds", "freeze_debit_card", "dispute_charge"]
        )

        engine = PolicyGateEngine(policy)
        brief = engine.evaluate_release(candidate=v_cand, baseline=v_base)

        st.markdown("---")
        st.markdown("### 📋 Release Recommendation")
        if brief.status == "READY_TO_SHIP":
            st.markdown('<div class="status-badge-ready">🟢 READY TO SHIP — All Policy Gates Passed</div>', unsafe_allow_html=True)
        elif brief.status == "BLOCKED":
            st.markdown('<div class="status-badge-blocked">🔴 RELEASE BLOCKED — Policy Regression / Security Violation Detected</div>', unsafe_allow_html=True)
        else:
            st.warning("🟡 REQUIRES PM EXCEPTION REVIEW — Marginal threshold breach.")

        if brief.hard_blockers:
            st.error(f"**Critical Blockers:** {'; '.join(brief.hard_blockers)}")

        st.markdown("#### Evaluated Gates")
        gate_table = []
        for g in brief.gates_evaluated:
            gate_table.append({
                "Gate": g.gate_name,
                "Status": "✅ PASS" if g.passed else ("🚫 BLOCKED" if g.is_hard_blocker else "❌ FAIL"),
                "Threshold": str(g.threshold),
                "Actual Result": str(g.actual_value),
                "Details": g.message
            })
        st.table(pd.DataFrame(gate_table))

        st.markdown("### 📄 Automated Release Decision Brief")
        st.markdown(brief.markdown_content)

        st.download_button(
            label="📥 Download Release Decision Brief (Markdown)",
            data=brief.markdown_content,
            file_name=f"release_decision_brief_{v_cand.variant_name}.md",
            mime="text/markdown"
        )


# -------------------------------------------------------------
# TAB 5: SHARE WITH COMMUNITY
# -------------------------------------------------------------
elif "5. Share with Community" in nav_choice:
    st.markdown('<div class="main-title">📤 Share with the AI Community</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Publish reusable Eval Packs, benchmark results, and adapters to help other AI builders.</div>', unsafe_allow_html=True)

    active_pack = st.session_state.get("active_pack")
    if active_pack:
        st.markdown(f"### Ready to Publish: **{active_pack.name}**")
        st.markdown("""
        How to contribute this pack to the official repository:
        1. Click below to copy or export your pack JSON.
        2. Place the file inside `agenteval/library/packs/<your_pack_slug>.json`.
        3. Open a Pull Request to [krishnamurthi-ramesh/AgentEval-Studio](https://github.com/krishnamurthi-ramesh/AgentEval-Studio).
        """)

        st.download_button(
            label="📦 Download Eval Pack JSON",
            data=json.dumps(active_pack.model_dump(), indent=2),
            file_name=f"{active_pack.id}.json",
            mime="application/json"
        )
        st.code(json.dumps(active_pack.model_dump(), indent=2), language="json")
    else:
        st.info("Select or generate an Eval Pack to export.")
