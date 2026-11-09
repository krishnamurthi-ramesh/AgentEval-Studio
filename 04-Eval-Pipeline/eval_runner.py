"""
Perplexity AI Eval Harness — Evaluation Runner
================================================
Runs test cases from the golden dataset against Perplexity AI,
records responses, and scores them using automated + LLM-judge evaluation.

Usage:
    python eval_runner.py --dataset ../02-Eval-Dataset/golden-dataset.csv --output results.json
    python eval_runner.py --dataset ../02-Eval-Dataset/golden-dataset.csv --output results.json --category "Current Events"
    python eval_runner.py --dataset ../02-Eval-Dataset/golden-dataset.csv --output results.json --limit 10

Requirements:
    pip install -r requirements.txt

Note: Since Perplexity doesn't have a free public API for evaluation,
      this script supports two modes:
      1. MANUAL mode: Generates a structured template for manual testing
      2. API mode: Uses Perplexity API (requires API key)
"""

import json
import csv
import argparse
import os
from datetime import datetime, timezone
from dataclasses import dataclass, asdict, field
from typing import Optional
import time


# ============================================================
# Data Models
# ============================================================

@dataclass
class EvalScores:
    factual_accuracy: int = 0       # FA: 1-5
    citation_accuracy: int = 0      # CA: 1-5
    freshness: int = 0              # FR: 1-5
    completeness: int = 0           # CO: 1-5
    harmlessness: int = 0           # HA: 1-5
    hedging: int = 0                # HE: 1-5
    format_usability: int = 0       # FU: 1-5
    latency: int = 0                # LA: 1-5

    def composite_score(self) -> float:
        """Calculate weighted composite score."""
        weights = {
            'factual_accuracy': 0.25,
            'citation_accuracy': 0.20,
            'freshness': 0.15,
            'completeness': 0.15,
            'harmlessness': 0.10,
            'hedging': 0.05,
            'format_usability': 0.05,
            'latency': 0.05,
        }
        total = sum(getattr(self, dim) * w for dim, w in weights.items())
        return round(total, 2)

    def grade(self) -> str:
        """Convert composite score to letter grade."""
        score = self.composite_score()
        if score >= 4.5:
            return "A"
        elif score >= 4.0:
            return "B"
        elif score >= 3.0:
            return "C"
        elif score >= 2.0:
            return "D"
        else:
            return "F"

    def has_critical_failure(self) -> bool:
        """Check for automatic failure conditions."""
        return self.harmlessness == 1 or self.citation_accuracy == 1


@dataclass
class TestCase:
    test_id: str
    category: str
    difficulty: str
    query: str
    ground_truth_answer: str
    ground_truth_source: str
    primary_dimension: str
    secondary_dimension: str = ""
    notes: str = ""


@dataclass
class EvalResult:
    test_id: str
    query: str
    category: str
    difficulty: str
    ground_truth: str
    timestamp: str = ""
    perplexity_model: str = "default"
    response_text: str = ""
    cited_sources: list = field(default_factory=list)
    latency_seconds: float = 0.0
    scores: dict = field(default_factory=dict)
    composite_score: float = 0.0
    grade: str = ""
    critical_failure: bool = False
    evaluator: str = "manual"
    notes: str = ""


# ============================================================
# Dataset Loader
# ============================================================

def load_dataset(filepath: str, category: Optional[str] = None, limit: Optional[int] = None) -> list[TestCase]:
    """Load test cases from the golden dataset CSV."""
    test_cases = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tc = TestCase(
                test_id=row.get('test_id', '').strip(),
                category=row.get('category', '').strip(),
                difficulty=row.get('difficulty', '').strip(),
                query=row.get('query', '').strip(),
                ground_truth_answer=row.get('ground_truth_answer', '').strip(),
                ground_truth_source=row.get('ground_truth_source', '').strip(),
                primary_dimension=row.get('primary_dimension', '').strip(),
                secondary_dimension=row.get('secondary_dimension', '').strip(),
                notes=row.get('notes', '').strip(),
            )
            if tc.test_id and tc.query:  # Skip empty rows
                if category is None or tc.category.lower() == category.lower():
                    test_cases.append(tc)
    
    if limit:
        test_cases = test_cases[:limit]
    
    print(f"📦 Loaded {len(test_cases)} test cases", end="")
    if category:
        print(f" (filtered: {category})", end="")
    print()
    
    return test_cases


# ============================================================
# Perplexity API Client (when API key is available)
# ============================================================

def query_perplexity_api(query: str, api_key: str) -> tuple[str, list[str], float]:
    """
    Query Perplexity API and return (response_text, cited_sources, latency_seconds).
    
    Requires: pip install requests
    API docs: https://docs.perplexity.ai/
    """
    import requests
    
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar",  # or "sonar-pro" for Pro tier
        "messages": [
            {"role": "user", "content": query}
        ],
        "return_citations": True
    }
    
    start_time = time.time()
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    latency = round(time.time() - start_time, 2)
    
    if response.status_code == 200:
        data = response.json()
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        citations = data.get("citations", [])
        return text, citations, latency
    else:
        print(f"  ❌ API error {response.status_code}: {response.text[:200]}")
        return f"[API ERROR: {response.status_code}]", [], latency


# ============================================================
# Manual Testing Mode
# ============================================================

def generate_manual_test_sheet(test_cases: list[TestCase], output_dir: str) -> str:
    """
    Generate a structured markdown file for manual testing.
    The evaluator copies queries into Perplexity, pastes responses, and scores.
    """
    filepath = os.path.join(output_dir, "manual-test-sheet.md")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# Manual Evaluation Sheet — Perplexity AI\n")
        f.write(f"## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("**Instructions:**\n")
        f.write("1. Copy each query into Perplexity AI (perplexity.ai)\n")
        f.write("2. Paste the full response below\n")
        f.write("3. List all cited source URLs\n")
        f.write("4. Record the approximate response time\n")
        f.write("5. Score each dimension (1-5) using the rubric in `03-Scoring-Rubric/`\n")
        f.write("6. Note any observations\n\n")
        f.write("---\n\n")
        
        for i, tc in enumerate(test_cases, 1):
            f.write(f"## Test {i}: `{tc.test_id}`\n\n")
            f.write(f"**Category:** {tc.category} | **Difficulty:** {tc.difficulty} | **Primary Dimension:** {tc.primary_dimension}\n\n")
            f.write(f"### Query\n```\n{tc.query}\n```\n\n")
            f.write(f"### Ground Truth\n> {tc.ground_truth_answer}\n\n")
            f.write(f"**Source:** {tc.ground_truth_source}\n\n")
            f.write(f"**Test notes:** {tc.notes}\n\n")
            f.write("### Perplexity Response\n")
            f.write("```\n[PASTE RESPONSE HERE]\n```\n\n")
            f.write("### Cited Sources\n")
            f.write("1. [URL]\n2. [URL]\n3. [URL]\n\n")
            f.write("### Response Time: ___ seconds\n\n")
            f.write("### Scores (1-5)\n")
            f.write("| Dimension | Score | Justification |\n")
            f.write("|-----------|-------|---------------|\n")
            f.write("| Factual Accuracy (FA) | /5 | |\n")
            f.write("| Citation Accuracy (CA) | /5 | |\n")
            f.write("| Freshness (FR) | /5 | |\n")
            f.write("| Completeness (CO) | /5 | |\n")
            f.write("| Harmlessness (HA) | /5 | |\n")
            f.write("| Hedging (HE) | /5 | |\n")
            f.write("| Format & Usability (FU) | /5 | |\n\n")
            f.write("### Notes & Observations\n")
            f.write("_[Write observations here]_\n\n")
            f.write("---\n\n")
    
    print(f"📝 Manual test sheet generated: {filepath}")
    return filepath


# ============================================================
# Results Processor
# ============================================================

def calculate_stats(results: list[dict]) -> dict:
    """Calculate aggregate statistics from evaluation results."""
    if not results:
        return {}
    
    stats = {
        "total_cases": len(results),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "overall": {},
        "by_category": {},
        "by_difficulty": {},
        "by_dimension": {},
        "critical_failures": [],
        "worst_performers": [],
    }
    
    # Overall stats
    scores = [r["composite_score"] for r in results if r.get("composite_score", 0) > 0]
    if scores:
        stats["overall"] = {
            "mean_score": round(sum(scores) / len(scores), 2),
            "min_score": round(min(scores), 2),
            "max_score": round(max(scores), 2),
            "median_score": round(sorted(scores)[len(scores) // 2], 2),
            "grade_distribution": {
                "A": sum(1 for s in scores if s >= 4.5),
                "B": sum(1 for s in scores if 4.0 <= s < 4.5),
                "C": sum(1 for s in scores if 3.0 <= s < 4.0),
                "D": sum(1 for s in scores if 2.0 <= s < 3.0),
                "F": sum(1 for s in scores if s < 2.0),
            },
            "pass_rate": round(sum(1 for s in scores if s >= 3.0) / len(scores) * 100, 1),
        }
    
    # By category
    categories = set(r.get("category", "") for r in results)
    for cat in categories:
        cat_scores = [r["composite_score"] for r in results 
                      if r.get("category") == cat and r.get("composite_score", 0) > 0]
        if cat_scores:
            stats["by_category"][cat] = {
                "count": len(cat_scores),
                "mean_score": round(sum(cat_scores) / len(cat_scores), 2),
                "pass_rate": round(sum(1 for s in cat_scores if s >= 3.0) / len(cat_scores) * 100, 1),
            }
    
    # By difficulty
    for diff in ["easy", "medium", "hard"]:
        diff_scores = [r["composite_score"] for r in results 
                       if r.get("difficulty", "").lower() == diff and r.get("composite_score", 0) > 0]
        if diff_scores:
            stats["by_difficulty"][diff] = {
                "count": len(diff_scores),
                "mean_score": round(sum(diff_scores) / len(diff_scores), 2),
                "pass_rate": round(sum(1 for s in diff_scores if s >= 3.0) / len(diff_scores) * 100, 1),
            }
    
    # By dimension (average score per dimension)
    dimensions = ["factual_accuracy", "citation_accuracy", "freshness", 
                   "completeness", "harmlessness", "hedging", "format_usability"]
    for dim in dimensions:
        dim_scores = [r.get("scores", {}).get(dim, 0) for r in results 
                      if r.get("scores", {}).get(dim, 0) > 0]
        if dim_scores:
            stats["by_dimension"][dim] = {
                "mean": round(sum(dim_scores) / len(dim_scores), 2),
                "min": min(dim_scores),
                "max": max(dim_scores),
                "below_3_count": sum(1 for s in dim_scores if s < 3),
            }
    
    # Critical failures
    for r in results:
        if r.get("critical_failure"):
            stats["critical_failures"].append({
                "test_id": r["test_id"],
                "query": r["query"][:100],
                "scores": r.get("scores", {}),
            })
    
    # Worst performers (bottom 10)
    scored_results = [(r["test_id"], r["composite_score"], r["query"][:80]) 
                      for r in results if r.get("composite_score", 0) > 0]
    scored_results.sort(key=lambda x: x[1])
    stats["worst_performers"] = [
        {"test_id": t[0], "score": t[1], "query": t[2]} 
        for t in scored_results[:10]
    ]
    
    return stats


def save_results(results: list[dict], stats: dict, output_path: str):
    """Save results and stats to JSON files."""
    output = {
        "metadata": {
            "eval_name": "Perplexity AI Eval Harness",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_cases": len(results),
            "tool_version": "1.0.0",
        },
        "statistics": stats,
        "results": results,
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Results saved to: {output_path}")
    
    # Also save stats separately for the dashboard
    stats_path = output_path.replace('.json', '_stats.json')
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Stats saved to: {stats_path}")


# ============================================================
# Manual Result Entry (Interactive)
# ============================================================

def interactive_scoring(test_cases: list[TestCase]) -> list[dict]:
    """Interactive CLI for manually entering scores after testing."""
    results = []
    
    print("\n" + "=" * 60)
    print("🎯 INTERACTIVE SCORING MODE")
    print("Enter scores for each test case after testing on Perplexity.")
    print("Type 'skip' to skip a test case, 'quit' to stop.")
    print("=" * 60 + "\n")
    
    for tc in test_cases:
        print(f"\n--- {tc.test_id} ({tc.category} / {tc.difficulty}) ---")
        print(f"Query: {tc.query[:100]}...")
        
        cmd = input("\nScore this case? (enter/skip/quit): ").strip().lower()
        if cmd == 'quit':
            break
        if cmd == 'skip':
            continue
        
        try:
            scores = EvalScores()
            print("Enter scores (1-5) for each dimension:")
            scores.factual_accuracy = int(input("  Factual Accuracy (FA): "))
            scores.citation_accuracy = int(input("  Citation Accuracy (CA): "))
            scores.freshness = int(input("  Freshness (FR): "))
            scores.completeness = int(input("  Completeness (CO): "))
            scores.harmlessness = int(input("  Harmlessness (HA): "))
            scores.hedging = int(input("  Hedging (HE): "))
            scores.format_usability = int(input("  Format & Usability (FU): "))
            
            latency = float(input("  Response time (seconds): "))
            if latency < 3:
                scores.latency = 5
            elif latency < 5:
                scores.latency = 4
            elif latency < 10:
                scores.latency = 3
            elif latency < 20:
                scores.latency = 2
            else:
                scores.latency = 1
            
            notes = input("  Notes (optional): ").strip()
            
            result = EvalResult(
                test_id=tc.test_id,
                query=tc.query,
                category=tc.category,
                difficulty=tc.difficulty,
                ground_truth=tc.ground_truth_answer,
                timestamp=datetime.now(timezone.utc).isoformat(),
                latency_seconds=latency,
                scores=asdict(scores),
                composite_score=scores.composite_score(),
                grade=scores.grade(),
                critical_failure=scores.has_critical_failure(),
                evaluator="manual",
                notes=notes,
            )
            
            results.append(asdict(result))
            print(f"  ✅ Score: {scores.composite_score()} ({scores.grade()})"
                  f"{' ⚠️ CRITICAL FAILURE' if scores.has_critical_failure() else ''}")
            
        except (ValueError, KeyboardInterrupt):
            print("  ⏭️ Skipped (invalid input)")
            continue
    
    return results


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Perplexity AI Eval Harness")
    parser.add_argument("--dataset", required=True, help="Path to golden dataset CSV")
    parser.add_argument("--output", default="results.json", help="Output file for results")
    parser.add_argument("--category", default=None, help="Filter by category")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of test cases")
    parser.add_argument("--mode", choices=["manual-sheet", "interactive", "api"], 
                        default="manual-sheet", help="Evaluation mode")
    parser.add_argument("--api-key", default=None, help="Perplexity API key (for api mode)")
    
    args = parser.parse_args()
    
    # Load dataset
    test_cases = load_dataset(args.dataset, args.category, args.limit)
    
    if not test_cases:
        print("❌ No test cases loaded. Check your dataset file.")
        return
    
    if args.mode == "manual-sheet":
        # Generate a manual testing sheet
        output_dir = os.path.dirname(args.output) or "."
        generate_manual_test_sheet(test_cases, output_dir)
        print("\n✅ Manual test sheet generated! Steps:")
        print("  1. Open the test sheet")
        print("  2. For each test case, query Perplexity and paste the response")
        print("  3. Score using the rubric")
        print("  4. Re-run with --mode interactive to enter scores")
    
    elif args.mode == "interactive":
        # Interactive scoring
        results = interactive_scoring(test_cases)
        if results:
            stats = calculate_stats(results)
            save_results(results, stats, args.output)
            print(f"\n📊 Summary:")
            print(f"   Cases scored: {stats.get('total_cases', 0)}")
            if stats.get('overall'):
                print(f"   Mean score: {stats['overall'].get('mean_score', 'N/A')}")
                print(f"   Pass rate: {stats['overall'].get('pass_rate', 'N/A')}%")
                print(f"   Critical failures: {len(stats.get('critical_failures', []))}")
    
    elif args.mode == "api":
        if not args.api_key:
            api_key = os.environ.get("PERPLEXITY_API_KEY")
            if not api_key:
                print("❌ API key required. Use --api-key or set PERPLEXITY_API_KEY env var.")
                return
        else:
            api_key = args.api_key
        
        results = []
        for i, tc in enumerate(test_cases, 1):
            print(f"\n[{i}/{len(test_cases)}] Testing: {tc.test_id} — {tc.query[:60]}...")
            response_text, citations, latency = query_perplexity_api(tc.query, api_key)
            
            # Create result with response (scores to be added via interactive mode or LLM judge)
            result = EvalResult(
                test_id=tc.test_id,
                query=tc.query,
                category=tc.category,
                difficulty=tc.difficulty,
                ground_truth=tc.ground_truth_answer,
                timestamp=datetime.now(timezone.utc).isoformat(),
                response_text=response_text,
                cited_sources=citations,
                latency_seconds=latency,
                evaluator="api-collected",
                notes="Response collected via API. Scores pending.",
            )
            results.append(asdict(result))
            
            # Rate limiting
            time.sleep(1)
        
        save_results(results, {}, args.output)
        print(f"\n✅ {len(results)} responses collected. Run --mode interactive to score them.")


if __name__ == "__main__":
    main()

