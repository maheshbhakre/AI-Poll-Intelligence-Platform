"""
Unit Tests for Data Validation Engine.
Validates missing values, duplicates, invalid ratings, category validity, and quality reports.
"""

import os
import pytest
import pandas as pd
from src.data_validation import run_data_validation, VALID_CATEGORIES


def test_data_validation_baseline(tmp_path):
    """Test data validation executes on standard dataset and generates valid CSV report."""
    test_csv = tmp_path / "test_poll.csv"
    test_report = tmp_path / "quality_report.csv"

    # Sample dataset
    df = pd.DataFrame({
        "Respondent_ID": ["R001", "R002", "R003"],
        "Age Group": ["18-24", "25-34", "35-44"],
        "Gender": ["Male", "Female", "Male"],
        "Region": ["Urban", "Rural", "Urban"],
        "Preferred Tool": ["Python", "Excel", "Power BI"],
        "Satisfaction (1-5)": [5, 4, 3],
        "Feedback": ["Great", "Good", "Okay"]
    })
    df.to_csv(test_csv, index=False)

    report_df, summary = run_data_validation(str(test_csv), str(test_report))

    assert os.path.exists(test_report)
    assert summary["total_records"] == 3
    assert summary["total_missing_cells"] == 0
    assert summary["duplicate_rows"] == 0
    assert summary["invalid_ratings_count"] == 0
    assert summary["completeness_rate"] == 100.0


def test_data_validation_anomaly_detection(tmp_path):
    """Test detection of missing values, duplicates, invalid ratings, and invalid categories."""
    anomaly_csv = tmp_path / "anomalous_poll.csv"
    test_report = tmp_path / "anomaly_report.csv"

    df = pd.DataFrame({
        "Respondent_ID": ["R001", "R001", "R003", "R004"],  # Duplicate ID
        "Age Group": ["18-24", "InvalidAge", "25-34", None],  # Invalid and missing
        "Gender": ["Male", "Female", "Martian", "Male"],      # Invalid category
        "Region": ["Urban", "Rural", "UnknownSpace", "Urban"],
        "Preferred Tool": ["Python", "Excel", "FakeTool", "Python"],
        "Satisfaction (1-5)": [5, 10, -2, "NotANumber"],      # Out-of-bounds & non-numeric
        "Feedback": ["Good", None, "Poor", "Okay"]
    })
    df.to_csv(anomaly_csv, index=False)

    report_df, summary = run_data_validation(str(anomaly_csv), str(test_report))

    assert summary["total_records"] == 4
    assert summary["total_missing_cells"] > 0
    assert summary["invalid_ratings_count"] == 3  # 10, -2, "NotANumber"
    assert summary["total_category_errors"] > 0
    assert summary["completeness_rate"] < 100.0
