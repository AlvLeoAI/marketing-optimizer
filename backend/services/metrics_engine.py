import pandas as pd
import numpy as np
from typing import List
from ..models.schemas import CampaignRecord, MetricResult, AnalysisResponse

def calculate_performance(data: List[CampaignRecord]) -> AnalysisResponse:
    """
    It receives validated data, transforms it into a DataFrame, and calculates business KPIs.
    """
    # 1. Convert list of Pydantic objects to Pandas DataFrame
    # We use model_dump() which is the modern way in Pydantic v2
    df = pd.DataFrame([record.model_dump() for record in data])
    
    if df.empty:
        return AnalysisResponse(summary=[], global_roas=0.0)

    # 2. Grouping by Channel
    metrics = df.groupby('channel').agg({
        'spend': 'sum',
        'revenue': 'sum',
        'conversions': 'sum',
        'clicks': 'sum'
    }).reset_index()

    # 3. Vectorized Calculations (Safe Handling of Division by Zero)
    # ROAS = Revenue / Spend
    metrics['roas'] = np.where(metrics['spend'] > 0, metrics['revenue'] / metrics['spend'], 0)
    
    # CPA = Spend / Conversions
    metrics['cpa'] = np.where(metrics['conversions'] > 0, metrics['spend'] / metrics['conversions'], 0)
    
    # CR = Conversions / Clicks (in percentage)
    metrics['cr'] = np.where(metrics['clicks'] > 0, (metrics['conversions'] / metrics['clicks']) * 100, 0)

    # 4. Generate a results list using business logic (Traffic Light)
    results = []
    for _, row in metrics.iterrows():
        # Simple business rule for the MVP
        status = "Good"
        if row['roas'] < 2.0: status = "Warning"
        if row['roas'] < 1.0: status = "Critical"
        
        results.append(MetricResult(
            channel=row['channel'],
            total_spend=round(row['spend'], 2),
            total_revenue=round(row['revenue'], 2),
            total_conversions=int(row['conversions']),
            roas=round(row['roas'], 2),
            cpa=round(row['cpa'], 2),
            conversion_rate=round(row['cr'], 2),
            recommendation_status=status
        ))
    
    # 5. Global Business KPI
    total_spend_all = metrics['spend'].sum()
    total_rev_all = metrics['revenue'].sum()
    global_roas = total_rev_all / total_spend_all if total_spend_all > 0 else 0.0

    return AnalysisResponse(summary=results, global_roas=round(global_roas, 2))