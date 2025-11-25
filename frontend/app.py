import sys
import os

# --- PATH FIX: Add project root to Python path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -------------------------------------------------

import streamlit as st
from frontend.components.sidebar import render_sidebar

# 1. Page Config
st.set_page_config(
    page_title="AI Marketing Optimizer",
    page_icon="🚀",
    layout="wide"
)

# 2. CSS PATH FIX (Use absolute path)
# This calculates the exact path: .../frontend/assets/style.css
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")

try:
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    # If it fails, don't break the app, just warn in console
    print(f"⚠️ Warning: CSS not found at {css_path}")

def main():
    # 3. Render Sidebar
    render_sidebar()
    
    # 4. Main Content
    st.title("Welcome to AI Marketing Optimizer 🧠")
    
    st.markdown("""
    ### Transform your Marketing Data into Actionable Insights
    
    This application uses **FastAPI** for high-performance processing and **AI Agents** to optimize your ad spend.
    
    #### 🏁 How to Start:
    1. **Navigate** to the `1_Upload_Data` page using the sidebar.
    2. **Upload** your campaign CSV file.
    3. **Analyze** the results in real-time.
    
    ---
    """)
    
    # 5. Call to Action & Helper
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("👈 **Start Here:** Click on `1_Upload_Data` in the sidebar menu.")
    
    with col2:
        sample_csv = "date,channel,spend,revenue,clicks,conversions\n2024-01-01,Facebook,100,200,500,10\n2024-01-01,Google,150,400,200,20"
        
        st.download_button(
            label="📄 Download Sample CSV Template",
            data=sample_csv,
            file_name="sample_campaigns.csv",
            mime="text/csv",
            help="Use this template to format your data correctly."
        )

if __name__ == "__main__":
    main()