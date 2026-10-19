# Project Audit: AI Poll Results Visualizer

**Audit Date**: October 2026  
**Auditor**: Senior Data Analyst, Survey Research Analyst & QA Architect  
**Project**: AI Poll Results Visualizer  
**Repository**: `AI-Poll-Results-Visualizer`  

---

## 1. Executive Summary

The **AI Poll Results Visualizer** is a Python and Streamlit-based survey analytics project designed to ingest, clean, explore, and visualize polling data regarding data science and AI tooling preferences. 

While the initial prototype successfully demonstrates end-to-end functionality (from synthetic data generation to basic Streamlit dashboards), this audit establishes the foundation for transforming the repository into an enterprise-grade, industry-standard poll analytics platform with rigorous data validation, modular analysis engines, comprehensive test suites, and executive reporting.

---

## 2. Current Architecture

```
AI-POLL-RESULTS-VISUALIZER/
├── app/
│   └── app.py                  # Monolithic Streamlit application
├── data/
│   ├── poll_data.csv           # Raw synthetic dataset (200 records)
│   └── cleaned_poll_data.csv   # Cleaned poll dataset (200 records)
├── docs/                       # Project documentation
├── images/                     # Matplotlib/Seaborn output figures
├── notebooks/                  # Exploratory notebooks (if any)
├── outputs/                    # Output summary tables & text reports
│   ├── insights_report.txt
│   ├── satisfaction_by_tool.csv
│   └── vote_share.csv
├── src/
│   ├── advanced_visuals.py     # Matplotlib bar/pie/heatmap charts
│   ├── analysis.py             # Basic descriptive aggregations
│   ├── data_cleaning.py        # Preliminary data cleaning pipeline
│   ├── data_generator.py       # Synthetic poll dataset generator
│   ├── eda_analysis.py         # Exploratory data plots
│   └── insights.py             # Basic rule-based recommendation generator
├── tests/                      # Automated unit test suite (pytest)
├── main.py                     # Environment check script
├── README.md                   # Repository documentation
└── requirements.txt            # Python dependencies
```

### Architectural Flow:
1. **Data Ingestion**: Synthetic data generated via `src/data_generator.py` or read from `data/poll_data.csv`.
2. **Preprocessing**: Handled in `src/data_cleaning.py` with pandas.
3. **Exploratory & Static Analysis**: Spread across `src/analysis.py`, `src/eda_analysis.py`, `src/advanced_visuals.py`, and `src/insights.py`.
4. **Interactive Dashboard**: Monolithic Streamlit app in `app/app.py` combining UI logic, filtering, chart generation, form submission, and text sentiment analysis.

---

## 3. Current Features

* **Synthetic Data Generation**: Reproducible creation of survey records with demographic traits (Age Group, Gender, Region), tool preference (Python, Excel, Power BI, R), satisfaction scores (1–5), and canned text feedback.
* **Basic Data Cleaning**: Deduplication, drop missing critical values, date conversion, and feedback length calculation.
* **Basic Survey Statistics**: Vote counts, tool preference percentages, average satisfaction scores, and simple cross-tabulations.
* **Static Visuals**: Matplotlib/Seaborn exports for vote shares, daily response timelines, demographic distributions, and satisfaction heatmaps.
* **Text Analytics**: WordCloud visual and TextBlob polarity scoring for user comments.
* **Streamlit Dashboard**:
  * Sidebar filters for tools and regions.
  * KPI metric cards (Total Responses, Avg Satisfaction, Top Tool, Top Share %).
  * Matplotlib and Streamlit native chart renderings.
  * In-dashboard response submission form appending to CSV.

---

## 4. Missing Features & Gaps Identified

1. **Automated Data Validation Engine**:
   - Absence of automated data schema validation, domain constraint checking, anomaly detection, and survey data quality metrics (e.g., completeness scores, duplicate respondent detection, rating bounds).
2. **Formal Survey Research Metrics**:
   - Lack of standard survey research KPIs (response completion rates, margin of error, Net Promoter/Satisfaction tiering, distribution skewness).
3. **Structured Demographic Intelligence**:
   - Demographic metrics are calculated ad-hoc without unified multi-dimensional reporting across Age, Gender, and Region combined with satisfaction and primary tool preference.
4. **In-Depth Satisfaction Analytics**:
   - Lack of statistical spread metrics (median, interquartile range, standard deviation, min/max satisfaction breakdown by tool and region).
5. **Robust Text & Feedback Analytics**:
   - Feedback processing relies on raw string splitting rather than clean tokenization, stopword removal, and structured sentiment distribution summary tables.
6. **Programmatic Executive Reporting**:
   - Insights were generated solely as unstructured plain text rather than machine-readable JSON structured reports (`outputs/executive_summary.json`).
7. **Automated Testing Suite**:
   - No pytest unit tests or integration tests existed to validate pipeline steps, data integrity, and metric computations.
8. **UI Modularity**:
   - The Streamlit application was monolithic without distinct, structured tabbed sections for Overview, Survey Metrics, Demographics, Satisfaction, Feedback, and Insights.

---

## 5. Code Quality Review

| Category | Finding | Severity | Recommendation |
| :--- | :--- | :--- | :--- |
| **Console Encoding** | Windows default `cp1252` encoding threw `UnicodeEncodeError` on emojis (`\u2705`) during terminal prints. | Medium | Standardize UTF-8 execution via environment settings and resilient print statements. |
| **Plot Blocking** | `plt.show()` in batch scripts blocked headless CLI execution without `MPLBACKEND=Agg`. | Medium | Configure non-interactive backend (`Agg`) and encapsulate chart generation into reusable plotting functions. |
| **Modularity & Reusability** | Code in `src/` consisted of standalone scripts with global variables rather than modular, importable functions. | High | Refactor core engines (`data_validation`, `survey_metrics`, `satisfaction_analysis`, `text_analysis`, `eda`, `insights_engine`) into modular callable functions and CLI entrypoints. |
| **Output Standardization** | Analysis outputs were scattered or incomplete without unified CSV and JSON artifacts. | High | Generate dedicated, structured CSVs and JSONs in `outputs/` for downstream BI and dashboards. |

---

## 6. Improvement Recommendations & Phase 1 Roadmap

1. **Build Data Validation Engine (`src/data_validation.py`)**:
   - Detect missing values, duplicates, out-of-range satisfaction ratings, invalid categories, and generate `outputs/data_quality_report.csv`.
2. **Build Survey Metrics Engine (`src/survey_metrics.py`)**:
   - Compute total responses, completion rates, popular/least popular options, popularity percentages, and output `outputs/survey_metrics.csv` and `outputs/demographic_analysis.csv`.
3. **Build Satisfaction Analysis Engine (`src/satisfaction_analysis.py`)**:
   - Compute mean, median, min, max, tool-wise, and region-wise satisfaction and output `outputs/satisfaction_report.csv`.
4. **Build Text Feedback Engine (`src/text_analysis.py`)**:
   - Compute feedback length statistics, common word frequency (stopwords removed), sentiment polarity distributions, and output `outputs/text_feedback_report.csv` and `outputs/sentiment_summary.csv`.
5. **Build Non-blocking EDA Module (`src/eda.py`)**:
   - Programmatically generate and save vote shares, rating distributions, regional preferences, and age group charts in `images/`.
6. **Build Insights Engine (`src/insights_engine.py`)**:
   - Extract top findings, statistics, recommendations, and output `outputs/executive_summary.json`.
7. **Upgrade Streamlit Dashboard (`app/app.py`)**:
   - Organize into clean, professional tabs: Overview, Survey Metrics, Demographic Analysis, Satisfaction Analysis, Feedback Analysis, and Insights.
8. **Implement Test Suite (`tests/`)**:
   - Create tests for data validation, survey metrics, and insights engine with full pytest coverage.
9. **Upgrade Documentation & GitHub Cleanliness**:
   - Polish `README.md`, run `compileall`, `pytest`, `pip check`, and ensure zero dead code or exposed secrets.
