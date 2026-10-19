"""
Exploratory Data Analysis (EDA) Module for AI Poll Results Visualizer.
Generates publication-quality charts for:
  - Vote Share Analysis
  - Rating / Satisfaction Distribution
  - Region vs Tool Analysis
  - Age Group vs Tool Analysis
Saves charts into images/ directory without blocking GUI windows.
"""

import os
import matplotlib
matplotlib.use('Agg')  # Headless non-blocking backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def generate_eda_visualizations(data_path="data/cleaned_poll_data.csv", output_dir="images"):
    """
    Generates core EDA visualizations and saves high-resolution figures.
    """
    if not os.path.exists(data_path):
        data_path = "data/poll_data.csv"
        
    df = pd.read_csv(data_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Global visual styling
    sns.set_theme(style="whitegrid", font_scale=1.1)
    palette = sns.color_palette("muted")
    generated_files = []

    # 1. Vote Share Analysis (Bar Chart with Percentages)
    plt.figure(figsize=(9, 5))
    tool_counts = df["Preferred Tool"].value_counts()
    total = len(df)
    percentages = (tool_counts / total) * 100
    
    ax = sns.barplot(x=tool_counts.index, y=tool_counts.values, hue=tool_counts.index, palette="Blues_r", legend=False)
    for i, v in enumerate(tool_counts.values):
        ax.text(i, v + (total * 0.015), f"{percentages.iloc[i]:.1f}%\n({v})", ha='center', fontweight='bold', fontsize=10)
        
    plt.title("Survey Vote Share by AI / Data Tool", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Preferred Tool", fontsize=12)
    plt.ylabel("Vote Count", fontsize=12)
    plt.ylim(0, max(tool_counts.values) * 1.15)
    plt.tight_layout()
    vote_share_path = os.path.join(output_dir, "vote_share_analysis.png")
    plt.savefig(vote_share_path, dpi=300)
    plt.close()
    generated_files.append(vote_share_path)

    # 2. Rating Distribution (Histogram with KDE)
    plt.figure(figsize=(8, 5))
    sat_col = "Satisfaction (1-5)"
    sns.histplot(df[sat_col], bins=5, discrete=True, kde=True, color="#4C72B0", shrink=0.8)
    plt.title("Distribution of Satisfaction Ratings (1–5)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Satisfaction Score", fontsize=12)
    plt.ylabel("Respondent Count", fontsize=12)
    plt.xticks(range(1, 6))
    plt.tight_layout()
    rating_dist_path = os.path.join(output_dir, "rating_distribution.png")
    plt.savefig(rating_dist_path, dpi=300)
    plt.close()
    generated_files.append(rating_dist_path)

    # 3. Region Analysis (Grouped & Stacked)
    if "Region" in df.columns:
        plt.figure(figsize=(9, 5))
        region_crosstab = pd.crosstab(df["Region"], df["Preferred Tool"], normalize="index") * 100
        ax_reg = region_crosstab.plot(kind="bar", stacked=True, colormap="viridis", figsize=(9, 5))
        plt.title("Regional Tool Preference Distribution (%)", fontsize=14, fontweight='bold', pad=15)
        plt.xlabel("Geographic Region", fontsize=12)
        plt.ylabel("Percentage Share (%)", fontsize=12)
        plt.legend(title="Tool", bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.xticks(rotation=0)
        plt.tight_layout()
        region_path = os.path.join(output_dir, "region_analysis.png")
        plt.savefig(region_path, dpi=300)
        plt.close()
        generated_files.append(region_path)

    # 4. Age Group Analysis
    if "Age Group" in df.columns:
        plt.figure(figsize=(9, 5))
        age_crosstab = pd.crosstab(df["Age Group"], df["Preferred Tool"])
        ax_age = age_crosstab.plot(kind="bar", colormap="crest", figsize=(9, 5))
        plt.title("Tool Preferences Segmented by Age Cohort", fontsize=14, fontweight='bold', pad=15)
        plt.xlabel("Age Cohort", fontsize=12)
        plt.ylabel("Respondent Count", fontsize=12)
        plt.legend(title="Tool", bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.xticks(rotation=0)
        plt.tight_layout()
        age_path = os.path.join(output_dir, "age_group_analysis.png")
        plt.savefig(age_path, dpi=300)
        plt.close()
        generated_files.append(age_path)

    return generated_files


if __name__ == "__main__":
    print("=" * 60)
    print("Running EDA Visual Generation Module...")
    print("=" * 60)
    files = generate_eda_visualizations()
    for f in files:
        print(f"  [SAVED] {f}")
    print("\n[SUCCESS] All EDA visualizations exported to images/")
