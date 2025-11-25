from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

# Prefix to group all integrations
router = APIRouter(prefix="/integrations", tags=["Integrations & Webhooks"])

# --- DATA MODEL (Validation) ---
# This ensures n8n sends us clean data
class ExternalLead(BaseModel):
    source: str  # Ex: "Facebook Ads", "Typeform", "Shopify"
    campaign_id: Optional[str] = None
    lead_email: EmailStr
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = {} # For flexible extra data

# --- WEBHOOK ENDPOINT ---
@router.post("/webhook/ingest-data")
async def ingest_external_data(lead: ExternalLead):
    """
    Receives real-time data from automation tools (n8n, Make, Zapier).
    """
    try:
        # Assign timestamp if not provided
        if not lead.timestamp:
            lead.timestamp = datetime.now()

        # 1. Simulate Processing (Here would go the DB save)
        print(f"🔔 NEW LEAD RECEIVED from {lead.source}: {lead.lead_email}")
        
        # 2. "Trigger" Logic (Automation Logic)
        # This demonstrates the "Systems Thinking" part of the offer
        response_action = "Data Logged"
        
        # Example: If the lead comes from a VIP campaign, mark priority
        if lead.metadata.get("is_vip") == True:
            print("🚀 VIP ALERT: Notifying sales team...")
            response_action += " + Priority Alert Sent"

        return {
            "status": "success",
            "message": "Webhook processed successfully",
            "action_taken": response_action,
            "data_received": {
                "source": lead.source,
                "email": lead.lead_email
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook Error: {str(e)}")