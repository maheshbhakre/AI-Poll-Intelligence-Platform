"""
Satisfaction Analysis Module for AI Poll Results Visualizer.
Calculates deep satisfaction analytics:
  - Mean, Median, Min, Max, Standard Deviation
  - Tool-wise Satisfaction
  - Region-wise Satisfaction
Generates: outputs/satisfaction_report.csv
"""

import os
import pandas as pd
import numpy as np


def compute_satisfaction_analysis(data_path="data/cleaned_poll_data.csv", output_path="outputs/satisfaction_report.csv"):
    """
    Computes statistical satisfaction metrics across the whole sample,
    as well as segmented by preferred tool and geographic region.
    """
    if not os.path.exists(data_path):
        data_path = "data/poll_data.csv"
        
    df = pd.read_csv(data_path)
    sat_col = "Satisfaction (1-5)"
    
    # Clean numerical column
    df[sat_col] = pd.to_numeric(df[sat_col], errors='coerce')
    df = df.dropna(subset=[sat_col])

    # 1. Overall Metrics
    overall_mean = round(float(df[sat_col].mean()), 2)
    overall_median = round(float(df[sat_col].median()), 2)
    overall_min = int(df[sat_col].min())
    overall_max = int(df[sat_col].max())
    overall_std = round(float(df[sat_col].std()), 2)

    rows = [
        {"Analysis Scope": "Overall Sample", "Segment": "All Respondents", "Mean": overall_mean, "Median": overall_median, "Min": overall_min, "Max": overall_max, "Std Dev": overall_std, "Sample Size": len(df)}
    ]

    # 2. Tool-wise Satisfaction
    tool_groups = df.groupby("Preferred Tool")[sat_col]
    for tool, group in tool_groups:
        rows.append({
            "Analysis Scope": "Tool-wise",
            "Segment": tool,
            "Mean": round(float(group.mean()), 2),
            "Median": round(float(group.median()), 2),
            "Min": int(group.min()),
            "Max": int(group.max()),
            "Std Dev": round(float(group.std()), 2) if len(group) > 1 else 0.0,
            "Sample Size": len(group)
        })

    # 3. Region-wise Satisfaction
    if "Region" in df.columns:
        region_groups = df.groupby("Region")[sat_col]
        for region, group in region_groups:
            rows.append({
                "Analysis Scope": "Region-wise",
                "Segment": region,
                "Mean": round(float(group.mean()), 2),
                "Median": round(float(group.median()), 2),
                "Min": int(group.min()),
                "Max": int(group.max()),
                "Std Dev": round(float(group.std()), 2) if len(group) > 1 else 0.0,
                "Sample Size": len(group)
            })

    report_df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    report_df.to_csv(output_path, index=False)

    summary_stats = {
        "overall_mean": overall_mean,
        "overall_median": overall_median,
        "overall_min": overall_min,
        "overall_max": overall_max,
        "overall_std": overall_std,
        "tool_breakdown": report_df[report_df["Analysis Scope"] == "Tool-wise"].to_dict(orient="records"),
        "region_breakdown": report_df[report_df["Analysis Scope"] == "Region-wise"].to_dict(orient="records")
    }

    return report_df, summary_stats


if __name__ == "__main__":
    print("=" * 60)
    print("Executing Satisfaction Analysis...")
    print("=" * 60)
    rep_df, stats = compute_satisfaction_analysis()
    print(rep_df.to_string(index=False))
    print("\n[SUCCESS] Generated outputs/satisfaction_report.csv")
