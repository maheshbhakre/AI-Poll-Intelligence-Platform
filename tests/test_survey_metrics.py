"""
Unit Tests for Survey Metrics & Demographic Analysis.
Validates metric computations, distributions, and demographic segmentations.
"""

import os
import pytest
import pandas as pd
from src.survey_metrics import compute_survey_metrics, compute_demographic_analysis
from src.satisfaction_analysis import compute_satisfaction_analysis


@pytest.fixture
def sample_survey_csv(tmp_path):
    csv_path = tmp_path / "sample_survey.csv"
    data = {
        "Respondent_ID": [f"R{i}" for i in range(1, 11)],
        "Age Group": ["18-24"] * 4 + ["25-34"] * 4 + ["35-44"] * 2,
        "Gender": ["Male", "Female"] * 5,
        "Region": ["Urban"] * 6 + ["Rural"] * 4,
        "Preferred Tool": ["Python"] * 6 + ["Excel"] * 3 + ["R"] * 1,
        "Satisfaction (1-5)": [5, 5, 4, 4, 3, 3, 2, 2, 4, 3],
        "Feedback": ["Loved it", "Great tool", "Super useful"] * 3 + ["Okay"]
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    return str(csv_path)


def test_survey_metrics_calculation(sample_survey_csv, tmp_path):
    """Validate core survey metrics, popular tools, and response rates."""
    out_csv = tmp_path / "metrics.csv"
    metrics_df, summary = compute_survey_metrics(sample_survey_csv, str(out_csv))

    assert os.path.exists(out_csv)
    assert summary["total_responses"] == 10
    assert summary["response_rate"] == 100.0
    assert summary["most_popular_tool"] == "Python"
    assert summary["most_popular_pct"] == 60.0
    assert summary["least_popular_tool"] == "R"
    assert summary["least_popular_pct"] == 10.0
    assert 1.0 <= summary["avg_satisfaction"] <= 5.0


def test_demographic_analysis(sample_survey_csv, tmp_path):
    """Validate demographic segmentation across age, gender, and region."""
    out_demo = tmp_path / "demographics.csv"
    demo_df = compute_demographic_analysis(sample_survey_csv, str(out_demo))

    assert os.path.exists(out_demo)
    assert not demo_df.empty
    assert "Demographic Dimension" in demo_df.columns
    assert "Most Popular Tool" in demo_df.columns
    assert set(demo_df["Demographic Dimension"].unique()).issubset({"Age Group", "Gender", "Region"})


def test_satisfaction_analysis(sample_survey_csv, tmp_path):
    """Validate statistical satisfaction metrics across overall, tool, and region segments."""
    out_sat = tmp_path / "satisfaction.csv"
    sat_df, summary = compute_satisfaction_analysis(sample_survey_csv, str(out_sat))

    assert os.path.exists(out_sat)
    assert summary["overall_min"] >= 1
    assert summary["overall_max"] <= 5
    assert summary["overall_mean"] > 0
    assert len(summary["tool_breakdown"]) == 3  # Python, Excel, R
