import sys
import os

# --- PATH FIX: Go up two levels to reach project root ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# --------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from frontend.components.sidebar import render_sidebar

# 1. Page Config
st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")

# 2. Load CSS
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
try:
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# 3. Sidebar
render_sidebar()

# 4. Main Content
st.title("📈 Performance Dashboard")

# --- SAFETY CHECK: Did the user upload data? ---
if "analysis_result" not in st.session_state or "raw_data" not in st.session_state:
    st.warning("⚠️ No data found. Please upload a CSV file first.")
    st.info("👈 Go to **Upload Data** in the sidebar to get started.")
    st.stop() # Stop execution here if no data

# --- GET DATA FROM SESSION ---
analysis = st.session_state["analysis_result"] # The JSON from Backend
raw_df = st.session_state["raw_data"]         # The Raw DataFrame for time charts

# Convert Backend Summary List to DataFrame for easy plotting
summary_df = pd.DataFrame(analysis["summary"])

# --- SECTION 1: HIGH LEVEL KPIS ---
st.subheader("Global Performance")

# Calculate totals
total_spend = summary_df['total_spend'].sum()
total_revenue = summary_df['total_revenue'].sum()
total_conversions = summary_df['total_conversions'].sum()
global_roas = analysis['global_roas']

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Spend", f"${total_spend:,.0f}")
col2.metric("Total Revenue", f"${total_revenue:,.0f}")
col3.metric("Conversions", f"{total_conversions:,}")
col4.metric("Global ROAS", f"{global_roas}x", delta="Target > 2.0x")

st.divider()

# --- SECTION 2: CHARTS ---
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("ROAS by Channel")
    # Bar Chart with Color Coding based on performance
    fig_bar = px.bar(
        summary_df,
        x='channel',
        y='roas',
        color='recommendation_status',
        color_discrete_map={
            'Good': '#00CC96',   # Green
            'Warning': '#FFA15A', # Orange
            'Critical': '#EF553B' # Red
        },
        text='roas',
        title="Efficiency per Channel (ROAS)"
    )
    fig_bar.update_traces(texttemplate='%{text:.2f}x', textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("Budget Allocation")
    # Donut Chart
    fig_pie = px.pie(
        summary_df,
        values='total_spend',
        names='channel',
        hole=0.4,
        title="Spend Distribution"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- SECTION 3: TIME SERIES (Using Raw Data) ---
st.subheader("Revenue Trend Over Time")

# Ensure date is datetime
if 'date' in raw_df.columns:
    raw_df['date'] = pd.to_datetime(raw_df['date'])
    # Group by Date and Channel
    daily_trend = raw_df.groupby(['date', 'channel'])['revenue'].sum().reset_index()
    
    fig_line = px.line(
        daily_trend,
        x='date',
        y='revenue',
        color='channel',
        markers=True,
        title="Daily Revenue Performance"
    )
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.warning("⚠️ 'date' column not found in raw data, skipping trend chart.")

# --- SECTION 4: DETAILED TABLE ---
with st.expander("View Detailed Metrics Table"):
    st.dataframe(
        summary_df.style.format({
            "total_spend": "${:,.2f}",
            "total_revenue": "${:,.2f}",
            "roas": "{:.2f}x",
            "cpa": "${:,.2f}",
            "conversion_rate": "{:.2f}%"
        }),
        use_container_width=True
    )