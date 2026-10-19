"""
Survey Metrics & Demographic Analytics Engine.
Computes core survey KPIs, response rates, distribution, and cross-demographic breakdowns.
Generates:
  - outputs/survey_metrics.csv
  - outputs/demographic_analysis.csv
"""

import os
import pandas as pd
import numpy as np


def compute_survey_metrics(data_path="data/cleaned_poll_data.csv", output_metrics_path="outputs/survey_metrics.csv"):
    """
    Computes core survey KPIs and tool popularity distributions.
    """
    if not os.path.exists(data_path):
        data_path = "data/poll_data.csv"
        
    df = pd.read_csv(data_path)
    
    total_responses = len(df)
    
    # Response Rate (Assumed sample frame = total responses with zero dropouts)
    valid_completed = df.dropna(subset=["Preferred Tool", "Satisfaction (1-5)"]).shape[0]
    response_rate = round((valid_completed / total_responses) * 100, 2) if total_responses > 0 else 0.0

    # Tool counts & popularity
    tool_counts = df["Preferred Tool"].value_counts()
    tool_pct = ((tool_counts / total_responses) * 100).round(2)
    
    most_popular_tool = tool_counts.idxmax()
    most_popular_count = int(tool_counts.max())
    most_popular_pct = tool_pct.max()

    least_popular_tool = tool_counts.idxmin()
    least_popular_count = int(tool_counts.min())
    least_popular_pct = tool_pct.min()

    # Average Satisfaction
    avg_satisfaction = round(df["Satisfaction (1-5)"].mean(), 2)

    # Build metrics rows
    metrics_rows = [
        {"Category": "Volume", "Metric": "Total Responses", "Value": str(total_responses), "Unit": "Count"},
        {"Category": "Engagement", "Metric": "Response Completion Rate", "Value": f"{response_rate}%", "Unit": "Percentage"},
        {"Category": "Preference", "Metric": "Most Popular Option", "Value": f"{most_popular_tool} ({most_popular_pct}%)", "Unit": "Tool"},
        {"Category": "Preference", "Metric": "Least Popular Option", "Value": f"{least_popular_tool} ({least_popular_pct}%)", "Unit": "Tool"},
        {"Category": "Satisfaction", "Metric": "Average Satisfaction", "Value": str(avg_satisfaction), "Unit": "Scale (1-5)"}
    ]

    for tool, count in tool_counts.items():
        pct = tool_pct[tool]
        metrics_rows.append({
            "Category": "Response Distribution",
            "Metric": f"Tool Popularity: {tool}",
            "Value": f"{count} votes ({pct}%)",
            "Unit": "Distribution"
        })

    metrics_df = pd.DataFrame(metrics_rows)
    os.makedirs(os.path.dirname(output_metrics_path), exist_ok=True)
    metrics_df.to_csv(output_metrics_path, index=False)

    summary = {
        "total_responses": total_responses,
        "response_rate": response_rate,
        "most_popular_tool": most_popular_tool,
        "most_popular_pct": most_popular_pct,
        "least_popular_tool": least_popular_tool,
        "least_popular_pct": least_popular_pct,
        "avg_satisfaction": avg_satisfaction,
        "distribution": tool_counts.to_dict()
    }

    return metrics_df, summary


def compute_demographic_analysis(data_path="data/cleaned_poll_data.csv", output_demo_path="outputs/demographic_analysis.csv"):
    """
    Analyzes survey responses segmented by demographic dimensions:
    Age Group, Gender, Region.
    Outputs: outputs/demographic_analysis.csv
    """
    if not os.path.exists(data_path):
        data_path = "data/poll_data.csv"
        
    df = pd.read_csv(data_path)
    total_responses = len(df)
    
    demo_columns = ["Age Group", "Gender", "Region"]
    records = []

    for dim in demo_columns:
        if dim not in df.columns:
            continue
            
        grouped = df.groupby(dim)
        for group_name, group_df in grouped:
            count = len(group_df)
            share_pct = round((count / total_responses) * 100, 2)
            
            # Most popular tool in this group
            tool_mode = group_df["Preferred Tool"].value_counts().idxmax()
            tool_mode_pct = round((group_df["Preferred Tool"].value_counts().max() / count) * 100, 1)
            
            # Avg satisfaction in this group
            avg_sat = round(group_df["Satisfaction (1-5)"].mean(), 2)

            records.append({
                "Demographic Dimension": dim,
                "Group": group_name,
                "Response Count": count,
                "Share (%)": f"{share_pct}%",
                "Most Popular Tool": f"{tool_mode} ({tool_mode_pct}%)",
                "Average Satisfaction": avg_sat
            })

    demo_df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(output_demo_path), exist_ok=True)
    demo_df.to_csv(output_demo_path, index=False)

    return demo_df


if __name__ == "__main__":
    print("=" * 60)
    print("Running Survey Metrics Engine...")
    print("=" * 60)
    m_df, m_sum = compute_survey_metrics()
    print(m_df.to_string(index=False))

    print("\n" + "=" * 60)
    print("Running Demographic Analysis...")
    print("=" * 60)
    d_df = compute_demographic_analysis()
    print(d_df.to_string(index=False))

    print("\n[SUCCESS] Generated outputs/survey_metrics.csv and outputs/demographic_analysis.csv")
