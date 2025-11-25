from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from ..services import ai_agent

# Create the router with the prefix "/ai"
router = APIRouter(prefix="/ai", tags=["AI Agent"])

# Define the expected Data Structure for the request
class AIRequest(BaseModel):
    summary_data: Dict[str, Any] # This receives the JSON summary from the Frontend

@router.post("/generate-insights")
async def ask_ai_agent(request: AIRequest):
    """
    Endpoint that receives marketing metrics and calls the Google Gemini Agent.
    Returns strategic recommendations in text format.
    """
    try:
        # Call the Service Layer (The brain)
        insights = ai_agent.generate_marketing_insights(request.summary_data)
        
        # Return the response wrapped in a JSON
        return {"response": insights}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))