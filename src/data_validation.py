"""
Data Validation Engine for AI Poll Results Visualizer.
Performs data quality checks including missing values, duplicates,
invalid ratings, category discrepancies, and survey completeness metrics.
Generates: outputs/data_quality_report.csv
"""

import os
import pandas as pd
import numpy as np


VALID_CATEGORIES = {
    "Age Group": ["18-24", "25-34", "35-44", "45-54", "55+"],
    "Gender": ["Male", "Female", "Other", "Non-Binary", "Unknown"],
    "Region": ["Urban", "Rural", "Suburban"],
    "Preferred Tool": ["Python", "Excel", "R", "Power BI", "Power Bi", "Tableau", "SQL"]
}


def run_data_validation(data_path="data/poll_data.csv", output_report_path="outputs/data_quality_report.csv"):
    """
    Validates poll survey dataset and generates a comprehensive quality report.
    
    Parameters:
        data_path (str): Path to input dataset.
        output_report_path (str): Path to output CSV report.
        
    Returns:
        tuple: (quality_summary_df, validation_details_dict)
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")

    df = pd.read_csv(data_path)
    total_records = len(df)
    
    # 1. Missing Value Analysis
    missing_counts = df.isnull().sum()
    total_missing_cells = int(missing_counts.sum())
    rows_with_missing = int(df.isnull().any(axis=1).sum())

    # 2. Duplicate Detection
    duplicate_rows = int(df.duplicated().sum())
    duplicate_ids = int(df["Respondent_ID"].duplicated().sum()) if "Respondent_ID" in df.columns else 0

    # 3. Invalid Rating Detection
    sat_col = "Satisfaction (1-5)"
    invalid_ratings_count = 0
    if sat_col in df.columns:
        numeric_sat = pd.to_numeric(df[sat_col], errors='coerce')
        invalid_ratings_count = int(numeric_sat.isna().sum() + ((numeric_sat < 1) | (numeric_sat > 5)).sum())

    # 4. Invalid Category Detection
    category_errors = {}
    total_category_errors = 0
    for col, allowed_values in VALID_CATEGORIES.items():
        if col in df.columns:
            # Case-insensitive check
            allowed_lower = [v.lower() for v in allowed_values]
            col_cleaned = df[col].astype(str).str.strip().str.lower()
            invalid_mask = ~col_cleaned.isin(allowed_lower) & df[col].notna()
            err_count = int(invalid_mask.sum())
            category_errors[col] = err_count
            total_category_errors += err_count

    # 5. Survey Quality & Completeness Checks
    completeness_rate = round(((total_records - rows_with_missing) / total_records * 100), 2) if total_records > 0 else 0.0
    validity_rate = round(((total_records - (invalid_ratings_count + total_category_errors + duplicate_rows)) / total_records * 100), 2) if total_records > 0 else 0.0

    # Compile Quality Metric rows
    report_rows = [
        {"Category": "Overview", "Metric": "Total Records Inspected", "Value": str(total_records), "Status": "PASS"},
        {"Category": "Missing Values", "Metric": "Total Missing Cells", "Value": str(total_missing_cells), "Status": "PASS" if total_missing_cells == 0 else "WARNING"},
        {"Category": "Missing Values", "Metric": "Rows with Missing Values", "Value": str(rows_with_missing), "Status": "PASS" if rows_with_missing == 0 else "WARNING"},
        {"Category": "Duplicates", "Metric": "Duplicate Rows", "Value": str(duplicate_rows), "Status": "PASS" if duplicate_rows == 0 else "FAIL"},
        {"Category": "Duplicates", "Metric": "Duplicate Respondent IDs", "Value": str(duplicate_ids), "Status": "PASS" if duplicate_ids == 0 else "FAIL"},
        {"Category": "Rating Validity", "Metric": "Out-of-Bounds / Invalid Ratings (1-5)", "Value": str(invalid_ratings_count), "Status": "PASS" if invalid_ratings_count == 0 else "FAIL"},
        {"Category": "Category Validity", "Metric": "Total Invalid Category Entries", "Value": str(total_category_errors), "Status": "PASS" if total_category_errors == 0 else "WARNING"},
        {"Category": "Survey Quality", "Metric": "Completeness Rate (%)", "Value": f"{completeness_rate}%", "Status": "PASS" if completeness_rate >= 95 else "WARNING"},
        {"Category": "Survey Quality", "Metric": "Overall Validity Rate (%)", "Value": f"{validity_rate}%", "Status": "PASS" if validity_rate >= 90 else "WARNING"}
    ]

    # Add column-wise missing details
    for col, count in missing_counts.items():
        if count > 0:
            report_rows.append({
                "Category": "Missing Detail",
                "Metric": f"Missing in '{col}'",
                "Value": str(count),
                "Status": "WARNING"
            })

    # Add category discrepancy details
    for col, count in category_errors.items():
        if count > 0:
            report_rows.append({
                "Category": "Category Detail",
                "Metric": f"Invalid Values in '{col}'",
                "Value": str(count),
                "Status": "WARNING"
            })

    report_df = pd.DataFrame(report_rows)

    os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
    report_df.to_csv(output_report_path, index=False)
    
    validation_summary = {
        "total_records": total_records,
        "total_missing_cells": total_missing_cells,
        "duplicate_rows": duplicate_rows,
        "invalid_ratings_count": invalid_ratings_count,
        "total_category_errors": total_category_errors,
        "completeness_rate": completeness_rate,
        "validity_rate": validity_rate
    }

    return report_df, validation_summary


if __name__ == "__main__":
    print("=" * 60)
    print("Executing Data Validation Engine...")
    print("=" * 60)
    df_report, summary = run_data_validation()
    print(df_report.to_string(index=False))
    print("\n[SUCCESS] Quality report generated at outputs/data_quality_report.csv")
