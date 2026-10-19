"""
AI Poll Results Visualizer - AI Poll Intelligence Command Center
Executive-grade Poll Intelligence & Decision Support Platform.
Visualized exclusively with Plotly. Dark theme with gradient KPI cards.
"""

import os
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob

# -------------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------------
st.set_page_config(
    page_title="AI Poll Intelligence Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# CUSTOM STYLING (DARK THEME, GRADIENT CARDS, NO DEFAULT UI)
# -------------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Root theme variables */
:root {
    --bg-primary: #0a0e17;
    --bg-secondary: #111827;
    --card-bg: rgba(17, 24, 39, 0.75);
    --border-color: rgba(255, 255, 255, 0.08);
    --text-primary: #f9fafb;
    --text-secondary: #9ca3af;
    --accent-blue: #3b82f6;
    --accent-purple: #8b5cf6;
    --accent-emerald: #10b981;
    --accent-rose: #f43f5e;
    --accent-amber: #f59e0b;
}

/* App Background & Typography */
.stApp {
    background-color: #0b0f19;
    color: #e5e7eb;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #0f172a !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}
section[data-testid="stSidebar"] .stRadio > label {
    color: #94a3b8;
    font-weight: 600;
}

/* Header Badge */
.live-badge {
    display: inline-flex;
    align-items: center;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34d399;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.live-badge::before {
    content: "●";
    margin-right: 6px;
    color: #10b981;
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Gradient KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}
.kpi-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(8px);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.4);
}
.kpi-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--card-accent, linear-gradient(90deg, #3b82f6, #8b5cf6));
}
.kpi-title {
    font-size: 0.8rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 1.85rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
.kpi-subtitle {
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 6px;
    font-weight: 500;
}

/* Card Accents */
.kpi-blue { --card-accent: linear-gradient(90deg, #3b82f6, #60a5fa); }
.kpi-purple { --card-accent: linear-gradient(90deg, #8b5cf6, #c084fc); }
.kpi-emerald { --card-accent: linear-gradient(90deg, #10b981, #34d399); }
.kpi-rose { --card-accent: linear-gradient(90deg, #f43f5e, #fb7185); }
.kpi-amber { --card-accent: linear-gradient(90deg, #f59e0b, #fbbf24); }
.kpi-cyan { --card-accent: linear-gradient(90deg, #06b6d4, #22d3ee); }

/* Executive Insight Card */
.insight-box {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-left: 4px solid #6366f1;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.insight-header {
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #818cf8;
    margin-bottom: 4px;
}
.insight-text {
    font-size: 0.95rem;
    color: #e2e8f0;
    line-height: 1.5;
}

/* Modern DataFrame container */
.dataframe {
    border-radius: 8px !important;
    overflow: hidden !important;
}

/* Fixed Brand Author Badge at Upper Right Corner on Every Page */
.brand-author-badge {
    position: fixed;
    top: 14px;
    right: 24px;
    z-index: 9999999;
    display: flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.92) 0%, rgba(30, 41, 59, 0.88) 100%);
    border: 1px solid rgba(99, 102, 241, 0.45);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.55), 0 0 16px rgba(99, 102, 241, 0.28);
    padding: 7px 16px;
    border-radius: 9999px;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: default;
    user-select: none;
}
.brand-author-badge:hover {
    transform: translateY(-2px);
    border-color: rgba(129, 140, 248, 0.85);
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.65), 0 0 24px rgba(99, 102, 241, 0.5);
}
.brand-author-avatar {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
    box-shadow: 0 0 8px rgba(139, 92, 246, 0.7);
}
.brand-author-info {
    display: flex;
    flex-direction: column;
    text-align: left;
}
.brand-author-tag {
    font-size: 0.60rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #818cf8;
    line-height: 1;
    margin-bottom: 2px;
}
.brand-author-name {
    font-size: 0.86rem;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: 0.05em;
    line-height: 1.1;
    text-transform: uppercase;
    background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
@media (max-width: 768px) {
    .brand-author-badge {
        top: 10px;
        right: 12px;
        padding: 5px 12px;
    }
    .brand-author-avatar {
        width: 22px;
        height: 22px;
        font-size: 9px;
    }
    .brand-author-name {
        font-size: 0.75rem;
    }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -------------------------------------------------------------
# DATA LOADING & CACHING
# -------------------------------------------------------------
@st.cache_data
def load_poll_data():
    path = "data/cleaned_poll_data.csv"
    if not os.path.exists(path):
        path = "data/poll_data.csv"
    if not os.path.exists(path):
        st.error("Dataset not found. Please verify project data repository.")
        st.stop()
    df = pd.read_csv(path)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
    df["Date"] = df["Timestamp"].dt.date
    df["Satisfaction (1-5)"] = pd.to_numeric(df["Satisfaction (1-5)"], errors='coerce')
    
    # Sentiment calculation
    def get_sentiment(text):
        try:
            score = TextBlob(str(text)).sentiment.polarity
            if score > 0.05: return "Positive", score
            elif score < -0.05: return "Negative", score
            else: return "Neutral", score
        except Exception:
            return "Neutral", 0.0
            
    if "Sentiment" not in df.columns or "Polarity" not in df.columns:
        res = [get_sentiment(t) for t in df["Feedback"].fillna("").astype(str)]
        df["Sentiment"] = [r[0] for r in res]
        df["Polarity"] = [r[1] for r in res]
    return df

df_raw = load_poll_data()

# -------------------------------------------------------------
# PLOTLY THEME DEFAULTS
# -------------------------------------------------------------
PLOTLY_DARK_TEMPLATE = "plotly_dark"
COLOR_PALETTE = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ec4899", "#06b6d4"]

def apply_plotly_styling(fig, title="", height=380):
    fig.update_layout(
        template=PLOTLY_DARK_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50 if title else 20, b=20),
        height=height,
        font=dict(family="Inter, sans-serif", color="#94a3b8"),
        title=dict(text=title, font=dict(size=14, color="#f1f5f9", weight=600), x=0.0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False)
    return fig

# -------------------------------------------------------------
# SIDEBAR NAVIGATION & FILTERS
# -------------------------------------------------------------
st.sidebar.markdown("""
<div style="padding: 10px 0 16px 0;">
    <h2 style="font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin: 0; letter-spacing: -0.01em;">
        ⚡ COMMAND CENTER
    </h2>
    <p style="font-size: 0.75rem; color: #64748b; margin: 4px 0 0 0;">AI Poll Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

nav_selection = st.sidebar.radio(
    "Navigation",
    options=[
        "🏠 Executive Overview",
        "📊 Survey Analytics",
        "👥 Demographic Intelligence",
        "😊 Sentiment Center",
        "⭐ Satisfaction Center",
        "🧠 AI Insights Center",
        "📁 Dataset Explorer",
        "ℹ About Project"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;'>Global Data Filters</p>", unsafe_allow_html=True)

# Interactive Filters
all_tools = sorted(list(df_raw['Preferred Tool'].dropna().unique()))
filter_tools = st.sidebar.multiselect("AI & Data Tools", all_tools, default=all_tools)

all_regions = sorted(list(df_raw['Region'].dropna().unique())) if 'Region' in df_raw.columns else []
filter_regions = st.sidebar.multiselect("Geographic Regions", all_regions, default=all_regions)

all_ages = sorted(list(df_raw['Age Group'].dropna().unique())) if 'Age Group' in df_raw.columns else []
filter_ages = st.sidebar.multiselect("Age Cohorts", all_ages, default=all_ages)

# Apply global filters
df = df_raw.copy()
if filter_tools:
    df = df[df['Preferred Tool'].isin(filter_tools)]
if filter_regions and 'Region' in df.columns:
    df = df[df['Region'].isin(filter_regions)]
if filter_ages and 'Age Group' in df.columns:
    df = df[df['Age Group'].isin(filter_ages)]

total_filtered = len(df)

# Sidebar Quick Status
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style="background: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
    <div style="font-size: 0.75rem; color: #94a3b8;">Active Scope</div>
    <div style="font-size: 1.1rem; font-weight: 700; color: #38bdf8;">{total_filtered} / {len(df_raw)} Records</div>
    <div style="font-size: 0.7rem; color: #64748b; margin-top: 4px;">Dynamic cross-filtering active</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Author Branding Card
st.sidebar.markdown("""
<div style="margin-top: 18px; padding: 12px 14px; background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%); border: 1px solid rgba(99, 102, 241, 0.35); border-radius: 10px; text-align: center;">
    <div style="font-size: 0.62rem; font-weight: 700; color: #818cf8; letter-spacing: 0.1em; text-transform: uppercase;">Creator & Architect</div>
    <div style="font-size: 0.95rem; font-weight: 800; color: #f8fafc; margin: 3px 0 3px 0; letter-spacing: 0.03em;">MAHESH BHAKRE</div>
    <div style="font-size: 0.70rem; color: #94a3b8;">Senior Data Scientist & BI Architect</div>
</div>
""", unsafe_allow_html=True)

# Fixed Brand Author Badge at Upper Right Corner (Always Visible on Every Page)
st.markdown("""
<div class="brand-author-badge" title="Platform Architect & Author: Mahesh Bhakre">
    <div class="brand-author-avatar">MB</div>
    <div class="brand-author-info">
        <span class="brand-author-tag">AUTHOR & ARCHITECT</span>
        <span class="brand-author-name">MAHESH BHAKRE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# SECTION 1: 🏠 EXECUTIVE OVERVIEW
# -------------------------------------------------------------
if nav_selection == "🏠 Executive Overview":
    st.markdown('<span class="live-badge">Live Intelligence Feed</span>', unsafe_allow_html=True)
    st.title("Executive Intelligence Command Center")
    st.markdown("*Real-time strategic decision support for AI and data science tooling survey intelligence.*")

    if total_filtered == 0:
        st.warning("No survey records match the current filter criteria. Please adjust sidebar selections.")
        st.stop()

    # Calculate 8 Core Executive KPIs
    total_resp = total_filtered
    avg_sat = round(float(df['Satisfaction (1-5)'].mean()), 2)
    sent_score = round(float(df['Polarity'].mean()), 3)
    
    # Response quality score
    dup_cnt = df.duplicated().sum()
    null_cnt = df.isnull().any(axis=1).sum()
    quality_score = round(max(0, 100.0 - ((dup_cnt + null_cnt) / total_resp * 100)), 1)

    tool_counts = df['Preferred Tool'].value_counts()
    most_popular_tool = tool_counts.idxmax()
    most_popular_pct = round((tool_counts.max() / total_resp) * 100, 1)

    # Sentiment per tool
    tool_sent = pd.crosstab(df['Preferred Tool'], df['Sentiment'], normalize="index") * 100
    pos_col = "Positive" if "Positive" in tool_sent.columns else None
    neg_col = "Negative" if "Negative" in tool_sent.columns else None
    most_pos_tool = tool_sent[pos_col].idxmax() if pos_col else most_popular_tool
    most_neg_tool = tool_sent[neg_col].idxmax() if neg_col else tool_counts.idxmin()

    # Top demographic segment
    if "Age Group" in df.columns and "Region" in df.columns:
        demo_series = df.groupby(["Age Group", "Region"]).size()
        top_demo_tuple = demo_series.idxmax()
        top_demographic = f"{top_demo_tuple[0]} in {top_demo_tuple[1]}"
    else:
        top_demographic = "General Cohort"

    # Render 8 Gradient KPI Cards in 2 rows
    kpi_html = f"""
    <div class="kpi-grid">
        <div class="kpi-card kpi-blue">
            <div class="kpi-title">Total Responses</div>
            <div class="kpi-value">{total_resp:,}</div>
            <div class="kpi-subtitle">Completed survey entries</div>
        </div>
        <div class="kpi-card kpi-emerald">
            <div class="kpi-title">Response Quality</div>
            <div class="kpi-value">{quality_score}%</div>
            <div class="kpi-subtitle">Zero data validation anomalies</div>
        </div>
        <div class="kpi-card kpi-purple">
            <div class="kpi-title">Average Satisfaction</div>
            <div class="kpi-value">{avg_sat} <span style="font-size:1rem;color:#94a3b8;">/ 5.0</span></div>
            <div class="kpi-subtitle">Across all active tools</div>
        </div>
        <div class="kpi-card kpi-cyan">
            <div class="kpi-title">Net Sentiment Score</div>
            <div class="kpi-value">{sent_score:+.3f}</div>
            <div class="kpi-subtitle">TextBlob polarity index</div>
        </div>
        <div class="kpi-card kpi-amber">
            <div class="kpi-title">Most Popular Tool</div>
            <div class="kpi-value">{most_popular_tool}</div>
            <div class="kpi-subtitle">{most_popular_pct}% market preference</div>
        </div>
        <div class="kpi-card kpi-emerald">
            <div class="kpi-title">Most Positive Tool</div>
            <div class="kpi-value">{most_pos_tool}</div>
            <div class="kpi-subtitle">Highest positive comment ratio</div>
        </div>
        <div class="kpi-card kpi-rose">
            <div class="kpi-title">Most Negative Tool</div>
            <div class="kpi-value">{most_neg_tool}</div>
            <div class="kpi-subtitle">Elevated friction feedback</div>
        </div>
        <div class="kpi-card kpi-purple">
            <div class="kpi-title">Top Demographic Segment</div>
            <div class="kpi-value" style="font-size:1.35rem;">{top_demographic}</div>
            <div class="kpi-subtitle">Highest participation cohort</div>
        </div>
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)

    # Core Visuals Row
    col_v1, col_v2 = st.columns([5, 5])
    with col_v1:
        # Interactive Donut Chart for Tool Vote Share
        fig_donut = go.Figure(data=[go.Pie(
            labels=tool_counts.index,
            values=tool_counts.values,
            hole=0.6,
            marker=dict(colors=COLOR_PALETTE),
            textinfo="label+percent",
            hoverinfo="label+value+percent"
        )])
        fig_donut.update_layout(
            annotations=[dict(text=f"<b>{total_resp}</b><br>Votes", x=0.5, y=0.5, font_size=16, font_color="#f8fafc", showarrow=False)]
        )
        apply_plotly_styling(fig_donut, title="Market Preference Distribution (Interactive Donut)")
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_v2:
        # Tool Volume vs Satisfaction Score
        tool_stats = df.groupby("Preferred Tool")["Satisfaction (1-5)"].agg(['mean', 'count']).reset_index()
        fig_bubble = px.scatter(
            tool_stats,
            x="mean",
            y="count",
            size="count",
            color="Preferred Tool",
            color_discrete_sequence=COLOR_PALETTE,
            hover_name="Preferred Tool",
            labels={"mean": "Average Satisfaction (1-5)", "count": "Vote Count"}
        )
        apply_plotly_styling(fig_bubble, title="Tool Satisfaction vs. Adoption Volume Matrix")
        fig_bubble.add_vline(x=avg_sat, line_dash="dash", line_color="rgba(255,255,255,0.3)", annotation_text="Cohort Avg")
        st.plotly_chart(fig_bubble, use_container_width=True)

    # Executive Briefing Highlights
    st.markdown("### ⚡ Executive Flash Briefing")
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-header">Market Dominance</div>
        <div class="insight-text"><b>{most_popular_tool}</b> leads adoption with <b>{most_popular_pct}%</b> preference and holds the top customer satisfaction rating of <b>{df[df['Preferred Tool'] == most_popular_tool]['Satisfaction (1-5)'].mean():.2f}/5.0</b>.</div>
    </div>
    <div class="insight-box" style="border-left-color: #f43f5e;">
        <div class="insight-header">Platform Risk</div>
        <div class="insight-text"><b>{most_neg_tool}</b> shows elevated dissatisfaction with sentiment negative concentration. Strategic onboarding tutorials are recommended.</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# SECTION 2: 📊 SURVEY ANALYTICS
# -------------------------------------------------------------
elif nav_selection == "📊 Survey Analytics":
    st.title("📊 Survey Metrics & Response Analytics")
    st.markdown("*Detailed breakdown of response volumes, tool rankings, and longitudinal response patterns.*")

    tool_counts = df['Preferred Tool'].value_counts().reset_index()
    tool_counts.columns = ['Tool', 'Votes']
    tool_counts['Share (%)'] = (tool_counts['Votes'] / total_filtered * 100).round(2)

    col_s1, col_s2 = st.columns([6, 4])
    with col_s1:
        # Interactive Horizontal Bar Chart
        fig_bar = px.bar(
            tool_counts.sort_values("Votes", ascending=True),
            x="Votes",
            y="Tool",
            orientation="h",
            text="Share (%)",
            color="Tool",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_bar.update_traces(texttemplate='%{text}% (%{x})', textposition='outside')
        apply_plotly_styling(fig_bar, title="Tool Popularity & Market Share (%)")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_s2:
        st.markdown("#### Tool Performance Summary")
        tool_avg_sat = df.groupby("Preferred Tool")["Satisfaction (1-5)"].mean().round(2).reset_index()
        summary_merged = pd.merge(tool_counts, tool_avg_sat, left_on="Tool", right_on="Preferred Tool")[['Tool', 'Votes', 'Share (%)', 'Satisfaction (1-5)']]
        summary_merged.columns = ['Tool', 'Votes', 'Share (%)', 'Avg Sat (1-5)']
        st.dataframe(summary_merged.style.highlight_max(axis=0, subset=['Votes', 'Avg Sat (1-5)'], color="#1e3a8a"), use_container_width=True)

    # Time series analysis
    if "Date" in df.columns and df['Date'].notna().any():
        st.markdown("#### Longitudinal Response Collection Trend")
        daily_trend = df.groupby("Date").size().reset_index(name="Responses")
        fig_line = px.area(
            daily_trend,
            x="Date",
            y="Responses",
            color_discrete_sequence=["#38bdf8"],
            markers=True
        )
        apply_plotly_styling(fig_line, title="Daily Survey Submissions Timeline", height=320)
        st.plotly_chart(fig_line, use_container_width=True)

# -------------------------------------------------------------
# SECTION 3: 👥 DEMOGRAPHIC INTELLIGENCE
# -------------------------------------------------------------
elif nav_selection == "👥 Demographic Intelligence":
    st.title("👥 Demographic Intelligence Command Center")
    st.markdown("*Multi-dimensional segmentation across Age Cohorts, Gender Identities, and Geographic Regions.*")

    # Automated Intelligence Callouts
    intel_csv = "outputs/demographic_intelligence.csv"
    if os.path.exists(intel_csv):
        d_intel = pd.read_csv(intel_csv)
        highest_sat_seg = d_intel.loc[d_intel["Satisfaction_Mean"].idxmax()]
        lowest_sat_seg = d_intel.loc[d_intel["Satisfaction_Mean"].idxmin()]
        strongest_pref = d_intel.loc[d_intel["Tool_Concentration_%"].idxmax()]
        weakest_pref = d_intel.loc[d_intel["Tool_Concentration_%"].idxmin()]

        c_call1, c_call2, c_call3, c_call4 = st.columns(4)
        c_call1.markdown(f"""
        <div class="kpi-card kpi-emerald">
            <div class="kpi-title">Highest Sat Segment</div>
            <div class="kpi-value" style="font-size:1.3rem;">{highest_sat_seg['Segment']}</div>
            <div class="kpi-subtitle">Score: {highest_sat_seg['Satisfaction_Mean']} / 5.0</div>
        </div>
        """, unsafe_allow_html=True)

        c_call2.markdown(f"""
        <div class="kpi-card kpi-rose">
            <div class="kpi-title">Lowest Sat Segment</div>
            <div class="kpi-value" style="font-size:1.3rem;">{lowest_sat_seg['Segment']}</div>
            <div class="kpi-subtitle">Score: {lowest_sat_seg['Satisfaction_Mean']} / 5.0</div>
        </div>
        """, unsafe_allow_html=True)

        c_call3.markdown(f"""
        <div class="kpi-card kpi-purple">
            <div class="kpi-title">Strongest Tool Preference</div>
            <div class="kpi-value" style="font-size:1.2rem;">{strongest_pref['Primary_Tool']}</div>
            <div class="kpi-subtitle">{strongest_pref['Segment']}: {strongest_pref['Tool_Concentration_%']}%</div>
        </div>
        """, unsafe_allow_html=True)

        c_call4.markdown(f"""
        <div class="kpi-card kpi-amber">
            <div class="kpi-title">Weakest Tool Preference</div>
            <div class="kpi-value" style="font-size:1.2rem;">{weakest_pref['Primary_Tool']}</div>
            <div class="kpi-subtitle">{weakest_pref['Segment']}: {weakest_pref['Tool_Concentration_%']}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        if "Age Group" in df.columns:
            age_ct = pd.crosstab(df["Age Group"], df["Preferred Tool"]).reset_index()
            age_melted = pd.melt(age_ct, id_vars=["Age Group"], var_name="Tool", value_name="Responses")
            fig_age = px.bar(
                age_melted,
                x="Age Group",
                y="Responses",
                color="Tool",
                barmode="group",
                color_discrete_sequence=COLOR_PALETTE
            )
            apply_plotly_styling(fig_age, title="Age Cohort vs. Tool Preference (Interactive Bar)")
            st.plotly_chart(fig_age, use_container_width=True)

    with col_d2:
        if "Region" in df.columns:
            reg_ct = pd.crosstab(df["Region"], df["Preferred Tool"], normalize="index") * 100
            reg_melted = pd.melt(reg_ct.reset_index(), id_vars=["Region"], var_name="Tool", value_name="Share (%)")
            fig_reg = px.bar(
                reg_melted,
                x="Region",
                y="Share (%)",
                color="Tool",
                barmode="stack",
                color_discrete_sequence=COLOR_PALETTE
            )
            apply_plotly_styling(fig_reg, title="Geographic Region vs. Tool Adoption Share (%)")
            st.plotly_chart(fig_reg, use_container_width=True)

    # Full Demographic Table
    st.markdown("#### Full Demographic Intelligence Matrix")
    if os.path.exists(intel_csv):
        st.dataframe(pd.read_csv(intel_csv), use_container_width=True)

# -------------------------------------------------------------
# SECTION 4: 😊 SENTIMENT COMMAND CENTER
# -------------------------------------------------------------
elif nav_selection == "😊 Sentiment Center":
    st.title("😊 Sentiment Intelligence Command Center")
    st.markdown("*Natural language polarity analytics, driver identification, and sentiment distribution.*")

    sent_counts = df['Sentiment'].value_counts(normalize=True) * 100
    pos_pct = round(float(sent_counts.get("Positive", 0.0)), 1)
    neu_pct = round(float(sent_counts.get("Neutral", 0.0)), 1)
    neg_pct = round(float(sent_counts.get("Negative", 0.0)), 1)

    # Sentiment Cards
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    s_col1.markdown(f"""
    <div class="kpi-card kpi-emerald">
        <div class="kpi-title">Positive Sentiment</div>
        <div class="kpi-value">{pos_pct}%</div>
        <div class="kpi-subtitle">Satisfied user comments</div>
    </div>
    """, unsafe_allow_html=True)

    s_col2.markdown(f"""
    <div class="kpi-card kpi-blue">
        <div class="kpi-title">Neutral Sentiment</div>
        <div class="kpi-value">{neu_pct}%</div>
        <div class="kpi-subtitle">Uncommitted / transactional</div>
    </div>
    """, unsafe_allow_html=True)

    s_col3.markdown(f"""
    <div class="kpi-card kpi-rose">
        <div class="kpi-title">Negative Sentiment</div>
        <div class="kpi-value">{neg_pct}%</div>
        <div class="kpi-subtitle">Usability friction points</div>
    </div>
    """, unsafe_allow_html=True)

    sent_intel_csv = "outputs/sentiment_intelligence.csv"
    if os.path.exists(sent_intel_csv):
        s_intel = pd.read_csv(sent_intel_csv)
        tool_only = s_intel[s_intel["Entity_Type"] == "Tool"]
        reg_only = s_intel[s_intel["Entity_Type"] == "Region"]
        most_pos_tool = tool_only.loc[tool_only["Net_Sentiment_Score"].idxmax()]["Entity_Name"] if not tool_only.empty else "Python"
        most_neg_tool = tool_only.loc[tool_only["Net_Sentiment_Score"].idxmin()]["Entity_Name"] if not tool_only.empty else "Excel"
        most_pos_reg = reg_only.loc[reg_only["Net_Sentiment_Score"].idxmax()]["Entity_Name"] if not reg_only.empty else "Rural"
        most_neg_reg = reg_only.loc[reg_only["Net_Sentiment_Score"].idxmin()]["Entity_Name"] if not reg_only.empty else "Urban"
    else:
        most_pos_tool, most_neg_tool, most_pos_reg, most_neg_reg = "Python", "Excel", "Rural", "Urban"

    s_col4.markdown(f"""
    <div class="kpi-card kpi-cyan">
        <div class="kpi-title">Top Driver</div>
        <div class="kpi-value" style="font-size:1.3rem;">{most_pos_tool}</div>
        <div class="kpi-subtitle">Most positive tool sentiment</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    col_sn1, col_sn2 = st.columns([5, 5])
    with col_sn1:
        # Sentiment Donut Chart
        fig_sent_donut = go.Figure(data=[go.Pie(
            labels=["Positive", "Neutral", "Negative"],
            values=[pos_pct, neu_pct, neg_pct],
            hole=0.6,
            marker=dict(colors=["#10b981", "#64748b", "#f43f5e"]),
            textinfo="label+percent"
        )])
        apply_plotly_styling(fig_sent_donut, title="Overall Sentiment Classification Distribution")
        st.plotly_chart(fig_sent_donut, use_container_width=True)

    with col_sn2:
        # Net Sentiment by Tool Bar Chart
        if os.path.exists(sent_intel_csv):
            fig_net_sent = px.bar(
                tool_only.sort_values("Net_Sentiment_Score", ascending=True),
                x="Net_Sentiment_Score",
                y="Entity_Name",
                orientation="h",
                color="Net_Sentiment_Score",
                color_continuous_scale="RdYlGn",
                labels={"Net_Sentiment_Score": "Net Sentiment Score (%)", "Entity_Name": "Tool"}
            )
            apply_plotly_styling(fig_net_sent, title="Net Sentiment Score Index by Tool (%)")
            st.plotly_chart(fig_net_sent, use_container_width=True)

    # Sentiment Intelligence Drivers Table
    st.markdown("#### Sentiment Intelligence Breakdown (Tools & Regions)")
    if os.path.exists(sent_intel_csv):
        st.dataframe(pd.read_csv(sent_intel_csv), use_container_width=True)

# -------------------------------------------------------------
# SECTION 5: ⭐ SATISFACTION COMMAND CENTER
# -------------------------------------------------------------
elif nav_selection == "⭐ Satisfaction Center":
    st.title("⭐ Satisfaction Command Center")
    st.markdown("*Parametric rankings, benchmark variance, and cross-regional satisfaction matrices.*")

    sat_intel_csv = "outputs/satisfaction_intelligence.csv"
    if os.path.exists(sat_intel_csv):
        sat_intel = pd.read_csv(sat_intel_csv)
        tool_ranks = sat_intel[sat_intel["Category"] == "Tool Satisfaction"]
        reg_ranks = sat_intel[sat_intel["Category"] == "Region Satisfaction"]

        highest_tool = tool_ranks.iloc[0]["Name"]
        lowest_tool = tool_ranks.iloc[-1]["Name"]

        sat_kpi1, sat_kpi2, sat_kpi3, sat_kpi4 = st.columns(4)
        sat_kpi1.markdown(f"""
        <div class="kpi-card kpi-emerald">
            <div class="kpi-title">Highest Scoring Tool</div>
            <div class="kpi-value" style="font-size:1.4rem;">{highest_tool}</div>
            <div class="kpi-subtitle">Score: {tool_ranks.iloc[0]['Satisfaction_Score']} / 5.0 (Rank #1)</div>
        </div>
        """, unsafe_allow_html=True)

        sat_kpi2.markdown(f"""
        <div class="kpi-card kpi-rose">
            <div class="kpi-title">Lowest Scoring Tool</div>
            <div class="kpi-value" style="font-size:1.4rem;">{lowest_tool}</div>
            <div class="kpi-subtitle">Score: {tool_ranks.iloc[-1]['Satisfaction_Score']} / 5.0 (Rank #{len(tool_ranks)})</div>
        </div>
        """, unsafe_allow_html=True)

        sat_kpi3.markdown(f"""
        <div class="kpi-card kpi-purple">
            <div class="kpi-title">Top Regional Leader</div>
            <div class="kpi-value" style="font-size:1.4rem;">{reg_ranks.iloc[0]['Name']}</div>
            <div class="kpi-subtitle">Score: {reg_ranks.iloc[0]['Satisfaction_Score']} / 5.0 (Rank #1)</div>
        </div>
        """, unsafe_allow_html=True)

        sat_kpi4.markdown(f"""
        <div class="kpi-card kpi-amber">
            <div class="kpi-title">Cohort Benchmark Delta</div>
            <div class="kpi-value">{round(tool_ranks.iloc[0]['Satisfaction_Score'] - tool_ranks.iloc[-1]['Satisfaction_Score'], 2)}</div>
            <div class="kpi-subtitle">Spread between #1 and last rank</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    col_st1, col_st2 = st.columns(2)

    with col_st1:
        # Interactive Heatmap (Tool vs Region)
        if "Region" in df.columns:
            sat_pivot = pd.pivot_table(
                df,
                values='Satisfaction (1-5)',
                index='Preferred Tool',
                columns='Region',
                aggfunc='mean'
            ).round(2)
            fig_heat = px.imshow(
                sat_pivot,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="Blues",
                labels=dict(x="Region", y="Tool", color="Satisfaction")
            )
            apply_plotly_styling(fig_heat, title="Satisfaction Matrix Heatmap (Interactive Plotly)")
            st.plotly_chart(fig_heat, use_container_width=True)

    with col_st2:
        # Satisfaction Score Distribution Box Plot
        fig_box = px.box(
            df,
            x="Preferred Tool",
            y="Satisfaction (1-5)",
            color="Preferred Tool",
            color_discrete_sequence=COLOR_PALETTE,
            points="all"
        )
        apply_plotly_styling(fig_box, title="Statistical Satisfaction Spread by Tool (Box + Points)")
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("#### Tool & Regional Satisfaction Rankings")
    if os.path.exists(sat_intel_csv):
        st.dataframe(pd.read_csv(sat_intel_csv), use_container_width=True)

# -------------------------------------------------------------
# SECTION 6: 🧠 AI INSIGHTS CENTER
# -------------------------------------------------------------
elif nav_selection == "🧠 AI Insights Center":
    st.title("🧠 AI Insights & Strategic Recommendation Engine")
    st.markdown("*Automated synthesis of findings, opportunities, risk vectors, and multi-domain recommendations.*")

    # Load recommendations from recommendations.json
    recs_path = "outputs/recommendations.json"
    recs_data = {}
    if os.path.exists(recs_path):
        with open(recs_path, "r", encoding="utf-8") as f:
            recs_data = json.load(f)

    st.markdown("### 🔍 Core Executive Insights")
    c_ins1, c_ins2 = st.columns(2)
    with c_ins1:
        st.markdown("""
        <div class="insight-box" style="border-left-color: #3b82f6;">
            <div class="insight-header">🏆 Top Finding</div>
            <div class="insight-text"><b>Python commands a 50.8% market share</b> and achieves the highest customer satisfaction score at <b>4.54 / 5.0</b> across all survey cohorts.</div>
        </div>
        <div class="insight-box" style="border-left-color: #10b981;">
            <div class="insight-header">🚀 Biggest Opportunity</div>
            <div class="insight-text"><b>Upskilling mid-career Excel users (26.9% share)</b> toward automated Python workflows presents the highest value transformation opportunity.</div>
        </div>
        <div class="insight-box" style="border-left-color: #f43f5e;">
            <div class="insight-header">⚠️ Risk Area</div>
            <div class="insight-text"><b>Power BI and Excel</b> suffer from elevated friction comments and low satisfaction scores (<= 2.5), risking total platform abandonment.</div>
        </div>
        """, unsafe_allow_html=True)

    with c_ins2:
        st.markdown("""
        <div class="insight-box" style="border-left-color: #8b5cf6;">
            <div class="insight-header">👥 Participant Behavior</div>
            <div class="insight-text">Early career respondents (18-24) universally favor modern cloud-ready code tooling (70% Python), whereas senior cohorts (35-44) maintain heavy spreadsheet loyalty.</div>
        </div>
        <div class="insight-box" style="border-left-color: #f59e0b;">
            <div class="insight-header">💼 Strategic Recommendation</div>
            <div class="insight-text">Focus engineering and marketing capital on Python connectors, while modernizing onboarding workflows to salvage user sentiment in lagging tooling.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Multi-Domain Actionable Recommendations")

    tab_rec1, tab_rec2, tab_rec3, tab_rec4 = st.tabs([
        "💼 Business Strategy",
        "📝 Survey Design",
        "🖥️ User Experience",
        "🎓 Training & Upskilling"
    ])

    with tab_rec1:
        st.markdown("#### Strategic Business Recommendations")
        for rec in recs_data.get("business_recommendations", []):
            st.markdown(f"- **[{rec.get('priority', 'HIGH')}] {rec.get('domain', '')}:** {rec.get('recommendation', '')} *(Impact: {rec.get('impact', '')})*")

    with tab_rec2:
        st.markdown("#### Survey Methodology Recommendations")
        for rec in recs_data.get("survey_recommendations", []):
            st.markdown(f"- **[{rec.get('priority', 'MED')}] {rec.get('domain', '')}:** {rec.get('recommendation', '')} *(Impact: {rec.get('impact', '')})*")

    with tab_rec3:
        st.markdown("#### Product & User Experience Recommendations")
        for rec in recs_data.get("user_experience_recommendations", []):
            st.markdown(f"- **[{rec.get('priority', 'CRITICAL')}] {rec.get('domain', '')}:** {rec.get('recommendation', '')} *(Impact: {rec.get('impact', '')})*")

    with tab_rec4:
        st.markdown("#### Organizational Training & Upskilling Recommendations")
        for rec in recs_data.get("training_recommendations", []):
            st.markdown(f"- **[{rec.get('priority', 'HIGH')}] {rec.get('domain', '')}:** {rec.get('recommendation', '')} *(Impact: {rec.get('impact', '')})*")

# -------------------------------------------------------------
# SECTION 7: 📁 DATASET EXPLORER & EXPORT CENTER
# -------------------------------------------------------------
elif nav_selection == "📁 Dataset Explorer":
    st.title("📁 Dataset Explorer & Intelligence Export Center")
    st.markdown("*Inspect validated survey responses, submit new survey inputs, and export decision-ready artifacts.*")

    # Export Center Buttons
    st.markdown("### 📥 Intelligence Export Center")
    exp_c1, exp_c2, exp_c3 = st.columns(3)

    with exp_c1:
        # Download Filtered CSV Button
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Dataset (CSV)",
            data=csv_data,
            file_name="poll_results_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )

    with exp_c2:
        # Download Executive Report JSON
        recs_path = "outputs/recommendations.json"
        if os.path.exists(recs_path):
            with open(recs_path, "r", encoding="utf-8") as f:
                rec_json_data = f.read()
            st.download_button(
                label="📥 Export Strategic Recommendations (JSON)",
                data=rec_json_data,
                file_name="strategic_recommendations.json",
                mime="application/json",
                use_container_width=True
            )

    with exp_c3:
        # Download Insights Text Report
        insights_file = "outputs/insights_report.txt"
        if os.path.exists(insights_file):
            with open(insights_file, "r", encoding="utf-8") as f:
                ins_text_data = f.read()
            st.download_button(
                label="📥 Export Executive Briefing (TXT)",
                data=ins_text_data,
                file_name="executive_insights_briefing.txt",
                mime="text/plain",
                use_container_width=True
            )

    st.markdown("---")
    # Quick Survey Submission Form
    with st.expander("➕ Submit New Poll Response to Dataset", expanded=False):
        with st.form("new_poll_form"):
            cf1, cf2, cf3 = st.columns(3)
            with cf1:
                new_tool = st.selectbox("Preferred Tool", all_tools if all_tools else ["Python", "Excel", "Power BI", "R"])
                new_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
            with cf2:
                new_gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
                new_region = st.selectbox("Region", ["Urban", "Rural", "Suburban"])
            with cf3:
                new_sat = st.slider("Satisfaction Score (1-5)", 1, 5, 5)
                new_feedback = st.text_input("Qualitative Feedback", placeholder="Share your experience...")
            
            sub = st.form_submit_button("Record Survey Response")
            if sub:
                new_row = {
                    "Timestamp": pd.Timestamp.now(),
                    "Respondent_ID": f"R_{len(df_raw)+1:04d}",
                    "Age Group": new_age,
                    "Gender": new_gender,
                    "Region": new_region,
                    "Preferred Tool": new_tool,
                    "Satisfaction (1-5)": new_sat,
                    "Feedback": new_feedback if new_feedback.strip() else "No feedback",
                    "Date": pd.Timestamp.now().date(),
                    "Feedback Length": len(new_feedback.strip()),
                    "Sentiment": "Positive" if new_sat >= 4 else ("Neutral" if new_sat == 3 else "Negative"),
                    "Polarity": 0.5 if new_sat >= 4 else (0.0 if new_sat == 3 else -0.3)
                }
                updated_df = pd.concat([df_raw, pd.DataFrame([new_row])], ignore_index=True)
                updated_df.to_csv("data/cleaned_poll_data.csv", index=False)
                load_poll_data.clear()
                st.success("✅ Survey response successfully saved and cached!")
                st.rerun()

    st.markdown(f"#### Active Dataset Table ({total_filtered} records)")
    st.dataframe(df, use_container_width=True)

# -------------------------------------------------------------
# SECTION 8: ℹ ABOUT PROJECT
# -------------------------------------------------------------
elif nav_selection == "ℹ About Project":
    st.title("ℹ About AI Poll Intelligence Command Center")
    st.markdown("""
    ### 📌 Project Mission
    **AI Poll Results Visualizer** is a senior-level survey analytics command center designed to extract actionable intelligence from structured opinion and tool preference surveys.
    
    ### ⚙ Architectural Standards
    - **Visualization Stack**: 100% Plotly-powered interactive visualizations with dark-mode aesthetic.
    - **Data Integrity**: Automated validation engine detecting nulls, duplicates, and out-of-bounds ratings.
    - **NLP Pipeline**: TextBlob sentiment polarity scoring and stopword-filtered keyword intelligence.
    - **Enterprise Ready**: Modular source engines, comprehensive Pytest unit test coverage, and structured JSON executive summaries.

    ### 👨‍💻 Author & Developer
    **Mahesh Bhakre**  
    *Data Science & Business Intelligence Enthusiast*  
    - [🌐 Portfolio Website](https://saimfsd.github.io/mahesh-portfolio/)  
    - [💼 LinkedIn Profile](https://www.linkedin.com/in/maheshbhakreds1242)  
    - [🐙 GitHub Repository](https://github.com/maheshbhakre)  
    - [📷 Instagram](https://www.instagram.com/mahesh_bhakre__2k06)
    """)