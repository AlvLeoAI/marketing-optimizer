import sys
import os

# --- PATH FIX: Go up two levels (../..) to reach the project root ---
# This allows importing from "frontend.components" without errors
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# --------------------------------------------------------------------

import streamlit as st
import pandas as pd
from frontend.components.sidebar import render_sidebar
from frontend.utils.api_client import send_csv_to_backend

# 1. Page Configuration
st.set_page_config(page_title="Upload Data", page_icon="📥", layout="wide")

# 2. CSS PATH FIX (Absolute Path)
# From "pages", we go up one level (..) to reach "frontend", then enter "assets"
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")

try:
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# 3. Render Sidebar
render_sidebar()

# 4. Main Content
st.title("📥 Data Ingestion")
st.markdown("Upload your campaign performance data (CSV) to initialize the analysis engine.")

# File Uploader Widget
uploaded_file = st.file_uploader("Drag and drop your CSV file here", type=["csv"])

if uploaded_file:
    # A. Show Preview
    st.subheader("📄 File Preview")
    try:
        df_preview = pd.read_csv(uploaded_file)
        st.dataframe(df_preview.head(), use_container_width=True)
        
        # IMPORTANT: Reset file pointer to the beginning before sending to API
        uploaded_file.seek(0)
        
        col1, col2 = st.columns([1, 4])
        
        # B. Action Button
        if col1.button("🚀 Process Data with AI", type="primary"):
            
            # Call Backend API
            result = send_csv_to_backend(uploaded_file)
            
            if result:
                # C. Success Handling
                st.toast("Analysis Complete!", icon="✅")
                st.success("Data successfully processed by the Backend Engine.")
                
                # Store results in Session State (Browser Memory)
                # This allows the Dashboard page to access this data later
                st.session_state["analysis_result"] = result
                st.session_state["raw_data"] = df_preview
                
                # Show immediate mini-summary
                st.info(f"Processed {len(result['summary'])} channels. Global ROAS: {result['global_roas']}x")
                
    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    # Empty State
    st.info("Awaiting file upload...")