import streamlit as st

def display_metric_row(metrics_list):
    """
    Renders a row of KPI cards dynamically.
    
    Args:
        metrics_list (list): List of dictionaries. Each dict should have:
                             {'label': str, 'value': str, 'delta': str (optional)}
    """
    # Create dynamic columns based on the number of metrics
    cols = st.columns(len(metrics_list))
    
    for col, metric in zip(cols, metrics_list):
        col.metric(
            label=metric.get("label"),
            value=metric.get("value"),
            delta=metric.get("delta"),
            delta_color="normal"
        )