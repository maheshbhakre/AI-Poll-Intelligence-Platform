"""
Unit Tests for AI Poll Intelligence Pipeline.
Validates demographic intelligence, satisfaction rankings, sentiment scores, and recommendations.
"""

import os
import json
import pytest
import pandas as pd
from src.intelligence_center import run_intelligence_pipeline


def test_intelligence_pipeline_execution(tmp_path):
    """Test full intelligence pipeline produces all 4 reports and valid data schemas."""
    mock_csv = tmp_path / "mock_poll.csv"
    mock_out = tmp_path / "outputs"

    df = pd.DataFrame({
        "Respondent_ID": [f"ID_{i}" for i in range(12)],
        "Age Group": ["18-24"] * 6 + ["25-34"] * 4 + ["35-44"] * 2,
        "Gender": ["Male", "Female"] * 6,
        "Region": ["Urban"] * 8 + ["Rural"] * 4,
        "Preferred Tool": ["Python"] * 6 + ["Excel"] * 4 + ["Power BI"] * 2,
        "Satisfaction (1-5)": [5, 5, 4, 4, 5, 4, 3, 3, 4, 3, 2, 2],
        "Feedback": ["Loved it", "Great tool", "Super useful", "Needs improvement", "Okay", "Good"] * 2
    })
    df.to_csv(mock_csv, index=False)

    results = run_intelligence_pipeline(str(mock_csv), str(mock_out))

    # Verify reports generated on disk
    assert os.path.exists(mock_out / "demographic_intelligence.csv")
    assert os.path.exists(mock_out / "satisfaction_intelligence.csv")
    assert os.path.exists(mock_out / "sentiment_intelligence.csv")
    assert os.path.exists(mock_out / "recommendations.json")

    # Verify KPIs
    kpis = results["kpi_summary"]
    assert kpis["total_responses"] == 12
    assert kpis["most_popular_tool"] == "Python"
    assert kpis["avg_satisfaction"] > 3.0
    assert 0 <= kpis["response_quality_score"] <= 100

    # Verify JSON structure
    with open(mock_out / "recommendations.json", "r", encoding="utf-8") as f:
        recs = json.load(f)
    assert "business_recommendations" in recs
    assert "survey_recommendations" in recs
    assert "user_experience_recommendations" in recs
    assert "training_recommendations" in recs
