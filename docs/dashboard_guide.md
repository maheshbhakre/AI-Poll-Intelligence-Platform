# 📖 AI Poll Intelligence Command Center: User & Operator Guide

**Document**: User & Operator Guide  
**Platform**: AI Poll Intelligence Command Center  
**Version**: 2.0 (Executive Edition)  
**Applicability**: Decision-Makers, Analysts, BI Engineers  

---

## 1. Introduction

The **AI Poll Intelligence Command Center** is a dark-themed, Plotly-powered executive analytics suite providing real-time visibility into survey feedback, tooling market share, and demographic satisfaction dynamics.

---

## 2. Quick Start & Launch Instructions

### 2.1 Prerequisites
Ensure the Python virtual environment is activated and dependencies are installed:
```bash
# Windows
.\venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 2.2 Launching the Application
Execute the following command from the project root:
```bash
streamlit run app/app.py
```
The application will launch automatically at `http://localhost:8501`.

---

## 3. Navigation Structure & Dashboard Pages

The platform features an intuitive, modern sidebar navigation dividing insights into 8 dedicated command views:

| Page | Primary Purpose | Key Visualizations |
| :--- | :--- | :--- |
| **🏠 Executive Overview** | High-level executive pulse check across all survey metrics. | 8 Gradient KPI cards, Market Share Donut Chart, Volume vs. Satisfaction Matrix, Flash Briefing. |
| **📊 Survey Analytics** | Deep dive into response volumes and market adoption share. | Horizontal Bar Share Chart, Longitudinal Area Timeline, Data Comparison Grid. |
| **👥 Demographic Intelligence** | Cross-cohort segmentation by Age, Gender, and Geographic Region. | Grouped Age Bar Chart, Stacked Regional Share Chart, Automated Segment Callout Cards. |
| **😊 Sentiment Center** | Natural Language sentiment polarity and driver analysis. | Sentiment Distribution Donut, Net Sentiment Index Diverging Bar, Entity Breakdown Table. |
| **⭐ Satisfaction Center** | Statistical satisfaction rankings and benchmark variances. | 2D Satisfaction Heatmap, Statistical Box & Point Spread Chart, Tool Rank Leaderboards. |
| **🧠 AI Insights Center** | Automated synthesis of findings, opportunities, and risks. | Multi-Domain Recommendation Tabs (Business, Survey, UX, Training). |
| **📁 Dataset Explorer** | Raw data inspection, live survey submission, and export center. | Interactive Data Grid, Survey Response Form, CSV/JSON/TXT Export Buttons. |
| **ℹ About Project** | Platform architectural overview, methodology, and author info. | System Architecture Diagram, Contact Links, and Version Metadata. |

---

## 4. Interactive Features

### 4.1 Global Dynamic Filters (Sidebar)
* **Tool Filter**: Multi-select specific platforms (Python, Excel, Power BI, R) to isolate comparative metrics.
* **Region Filter**: Toggle between Urban and Rural cohorts.
* **Age Filter**: Filter by 18–24, 25–34, and 35–44 cohorts.
* *Note: All charts, KPI cards, and statistical grids update instantaneously upon filter selection.*

### 4.2 Plotly Interactive Capabilities
Every chart is rendered exclusively via Plotly:
* **Hover Tooltips**: Inspect precise values, percentages, and segment names.
* **Pan & Zoom**: Focus on specific sub-ranges in timeline and distribution charts.
* **Legend Isolation**: Double-click on any legend entry to isolate that specific tool or cohort.
* **Image Snapshot**: Click the camera icon in the upper-right corner of any Plotly visual to download a high-resolution PNG snapshot.

### 4.3 Intelligence Export Center (Dataset Explorer Page)
* **Download Filtered Dataset (CSV)**: Export the actively filtered dataset for external analysis.
* **Export Strategic Recommendations (JSON)**: Download the structured recommendation package.
* **Export Executive Briefing (TXT)**: Download a plain-text executive brief for email and presentation distribution.

### 4.4 Live Response Submission Form
Navigate to **📁 Dataset Explorer** to test live survey ingestion. Responses are validated and appended directly to the database with immediate dashboard re-rendering.

---

## 5. Troubleshooting & Support

* **Port Already in Use**: If port 8501 is occupied, specify an alternative port:
  ```bash
  streamlit run app/app.py --server.port 8502
  ```
* **Encoding Warnings on Windows**: Launch PowerShell with UTF-8 encoding enabled:
  ```powershell
  $env:PYTHONIOENCODING="utf-8"
  ```
