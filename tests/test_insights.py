"""
Unit Tests for Executive Insights Engine.
Validates structured summary output, top findings, and recommendation generation.
"""

import os
import json
import pytest
import pandas as pd
from src.insights_engine import generate_executive_insights


@pytest.fixture
def mock_poll_data(tmp_path):
    path = tmp_path / "poll.csv"
    df = pd.DataFrame({
        "Respondent_ID": [f"ID_{i}" for i in range(20)],
        "Age Group": ["18-24"] * 10 + ["25-34"] * 5 + ["35-44"] * 5,
        "Gender": ["Male", "Female"] * 10,
        "Region": ["Urban"] * 12 + ["Rural"] * 8,
        "Preferred Tool": ["Python"] * 12 + ["Excel"] * 5 + ["Power BI"] * 2 + ["R"] * 1,
        "Satisfaction (1-5)": [5] * 10 + [4] * 5 + [3] * 3 + [2] * 2,
        "Feedback": ["Excellent"] * 10 + ["Good"] * 5 + ["Okay"] * 5
    })
    df.to_csv(path, index=False)
    return str(path)


def test_executive_insights_structure(mock_poll_data, tmp_path):
    """Test executive insights engine produces valid JSON schema with all expected keys."""
    json_path = tmp_path / "exec_summary.json"
    result = generate_executive_insights(mock_poll_data, str(json_path))

    assert os.path.exists(json_path)

    # Verify JSON structure
    with open(json_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert "survey_summary" in loaded
    assert "key_statistics" in loaded
    assert "top_findings" in loaded
    assert "actionable_recommendations" in loaded

    assert loaded["survey_summary"]["total_responses"] == 20
    assert loaded["survey_summary"]["most_preferred_tool"] == "Python"
    assert len(loaded["top_findings"]) >= 3
    assert len(loaded["actionable_recommendations"]) >= 3
