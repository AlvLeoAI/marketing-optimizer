from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import date

# --- INPUTS (What's included in the CSV) ---

class CampaignRecord(BaseModel):
    """
    Represents a clean row from the CSV file.
    Pydantic automatically converts strings to numbers.

    """
    date: date
    channel: str
    campaign_name: Optional[str] = "General"
    
    # Validations: We do not allow negative numbers
    spend: float = Field(..., ge=0)
    revenue: float = Field(..., ge=0)
    clicks: int = Field(..., ge=0)
    conversions: int = Field(..., ge=0)
    
    class Config:
        from_attributes = True

# --- OUTPUTS (What we return to the Dashboard) ---

class MetricResult(BaseModel):
    """Metrics calculated per channel"""
    channel: str
    total_spend: float
    total_revenue: float
    total_conversions: int
    roas: float
    cpa: float
    conversion_rate: float
    recommendation_status: str  # Example: "Good", "Warning", "Critical"

class AnalysisResponse(BaseModel):
    """The complete final API response"""
    summary: List[MetricResult]
    global_roas: float