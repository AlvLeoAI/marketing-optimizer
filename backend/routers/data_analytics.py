from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import numpy as np
import io
from typing import List
from ..services import metrics_engine
from ..models.schemas import CampaignRecord, AnalysisResponse

# Create the router instance
router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.post("/upload-csv", response_model=AnalysisResponse)
async def analyze_csv_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a CSV file.
    It validates the structure and returns calculated performance metrics.
    """
    # 1. Validate File Extension
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are accepted.")
    
    try:
        # 2. Read file content into a Pandas DataFrame
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # 3. Data Cleaning: Normalize column names
        # Example: "  Revenue " -> "revenue"
        df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
        
        # 4. Validate Required Columns
        required_columns = {'date', 'channel', 'spend', 'revenue', 'clicks', 'conversions'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns in CSV: {missing}"
            )

        # 5. Handle missing values (NaN)
        # Pydantic does not like NaN, so we convert them to None or 0
        df = df.replace({np.nan: None})
        
        # 6. Convert DataFrame to List of Dictionaries
        records_dicts = df.to_dict(orient='records')
        
        # 7. Validate Data Types using Pydantic
        # This loop checks every row against the CampaignRecord schema
        try:
            validated_data = [CampaignRecord(**record) for record in records_dicts]
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Data validation error: {str(e)}")
        
        # 8. Calculate Metrics using the Service Layer
        results = metrics_engine.calculate_performance(validated_data)
        
        return results

    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")