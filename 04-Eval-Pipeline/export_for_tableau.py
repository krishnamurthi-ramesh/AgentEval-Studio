"""
Tableau Public Data Exporter
===========================
Transforms evaluation JSON / raw test results into Tableau-ready flat CSV files.

Outputs:
1. eval_tableau_summary.csv: One row per query test case (Wide format)
2. eval_tableau_dimensions.csv: Normalized dimensions (Long format for Tableau parameter switches)
"""

import json
import csv
import os
import argparse
from datetime import datetime

def export_for_tableau(json_path: str, output_dir: str):
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = data.get("results", [])
    if not results:
        print("No results found in JSON file.")
        return

    os.makedirs(output_dir, exist_ok=True)
    wide_csv_path = os.path.join(output_dir, "eval_tableau_summary.csv")
    long_csv_path = os.path.join(output_dir, "eval_tableau_dimensions.csv")

    # 1. Wide Format Export
    fieldnames_wide = [
        "test_id", "category", "difficulty", "primary_dimension", 
        "query", "ground_truth", "timestamp", "perplexity_model", 
        "latency_seconds", "composite_score", "grade", "critical_failure",
        "factual_accuracy", "citation_accuracy", "freshness", 
        "completeness", "harmlessness", "hedging", "format_usability",
        "latency_score", "evaluator", "notes"
    ]

    with open(wide_csv_path, 'w', newline='', encoding='utf-8') as f_wide:
        writer = csv.DictWriter(f_wide, fieldnames=fieldnames_wide)
        writer.writeheader()

        for r in results:
            scores = r.get("scores", {})
            row = {
                "test_id": r.get("test_id", ""),
                "category": r.get("category", ""),
                "difficulty": r.get("difficulty", ""),
                "primary_dimension": r.get("primary_dimension", ""),
                "query": r.get("query", ""),
                "ground_truth": r.get("ground_truth", ""),
                "timestamp": r.get("timestamp", datetime.now().isoformat()),
                "perplexity_model": r.get("perplexity_model", "Perplexity Sonar"),
                "latency_seconds": r.get("latency_seconds", 0.0),
                "composite_score": r.get("composite_score", 0.0),
                "grade": r.get("grade", "N/A"),
                "critical_failure": "True" if r.get("critical_failure") else "False",
                "factual_accuracy": scores.get("factual_accuracy", 0),
                "citation_accuracy": scores.get("citation_accuracy", 0),
                "freshness": scores.get("freshness", 0),
                "completeness": scores.get("completeness", 0),
                "harmlessness": scores.get("harmlessness", 0),
                "hedging": scores.get("hedging", 0),
                "format_usability": scores.get("format_usability", 0),
                "latency_score": scores.get("latency", 0),
                "evaluator": r.get("evaluator", "Manual"),
                "notes": r.get("notes", "")
            }
            writer.writerow(row)

    print(f"✅ Generated Wide Dataset for Tableau: {wide_csv_path}")

    # 2. Long Format Export (Perfect for Category-to-Dimension Heatmaps & Radar Charts)
    dim_weights = {
        "Factual Accuracy": 0.25,
        "Citation Accuracy": 0.20,
        "Freshness": 0.15,
        "Completeness": 0.15,
        "Harmlessness": 0.10,
        "Hedging": 0.05,
        "Format & Usability": 0.05,
        "Latency": 0.05
    }

    dim_mapping = {
        "factual_accuracy": "Factual Accuracy",
        "citation_accuracy": "Citation Accuracy",
        "freshness": "Freshness",
        "completeness": "Completeness",
        "harmlessness": "Harmlessness",
        "hedging": "Hedging",
        "format_usability": "Format & Usability",
        "latency": "Latency"
    }

    fieldnames_long = [
        "test_id", "category", "difficulty", "perplexity_model",
        "dimension_name", "dimension_score", "dimension_weight",
        "is_below_acceptable_threshold", "composite_score", "grade"
    ]

    with open(long_csv_path, 'w', newline='', encoding='utf-8') as f_long:
        writer = csv.DictWriter(f_long, fieldnames=fieldnames_long)
        writer.writeheader()

        for r in results:
            scores = r.get("scores", {})
            for key, display_name in dim_mapping.items():
                score_val = scores.get(key, 0)
                writer.writerow({
                    "test_id": r.get("test_id", ""),
                    "category": r.get("category", ""),
                    "difficulty": r.get("difficulty", ""),
                    "perplexity_model": r.get("perplexity_model", "Perplexity Sonar"),
                    "dimension_name": display_name,
                    "dimension_score": score_val,
                    "dimension_weight": dim_weights.get(display_name, 0.0),
                    "is_below_acceptable_threshold": "Yes" if score_val < 3 else "No",
                    "composite_score": r.get("composite_score", 0.0),
                    "grade": r.get("grade", "N/A")
                })

    print(f"✅ Generated Long Dataset for Tableau: {long_csv_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Eval data for Tableau")
    parser.add_argument("--input", default="results.json", help="Path to evaluation results JSON")
    parser.add_argument("--outdir", default="../05-Dashboard/tableau-data", help="Output directory for CSVs")
    args = parser.parse_args()

    export_for_tableau(args.input, args.outdir)

