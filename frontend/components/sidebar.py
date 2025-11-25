import streamlit as st
from frontend.utils.api_client import get_health_check

def render_sidebar():
    with st.sidebar:
        st.header("🚀 AI Marketing Optimizer")
        st.caption("v1.0.0 | Powered by FastAPI")
        
        st.divider()
        
        # Live Backend Status Check
        if "backend_status" not in st.session_state:
            health = get_health_check()
            st.session_state["backend_status"] = "Online 🟢" if health else "Offline 🔴"
        
        st.markdown(f"**System Status:** {st.session_state['backend_status']}")
        
        st.divider()
        
        st.markdown("""
        **Navigation:**
        1. 📥 **Upload Data:** Ingest CSV
        2. 📈 **Dashboard:** Visual Analytics
        3. 🤖 **AI Agent:** Optimization
        """)
        
        st.info("Ensure `uvicorn` is running in the background.")