import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Configure Gemini API
GENAI_KEY = os.getenv("GEMINI_API_KEY")
if not GENAI_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY not found in .env")

# Model Configuration
try:
    genai.configure(api_key=GENAI_KEY)
except Exception as e:
    print(f"⚠️ Error configuring Gemini: {e}")

def get_available_model():
    """
    Dynamically finds a working model for the provided API Key.
    """
    try:
        # List all models available to this API Key
        models = list(genai.list_models())
        
        # Filter for models that support text generation ('generateContent')
        # We prefer 'gemini-1.5-flash' or 'gemini-pro'
        generative_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        
        print(f"🔍 Available Models for this Key: {generative_models}")
        
        # Priority list
        priorities = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        
        for priority in priorities:
            if priority in generative_models:
                # The library expects the name without 'models/' prefix sometimes, 
                # but list_models returns with it. We strip it for safety.
                return priority.replace('models/', '')
        
        # Fallback: Just take the first one available
        if generative_models:
            return generative_models[0].replace('models/', '')
            
        return 'gemini-1.5-flash' # Default blind hope
        
    except Exception as e:
        print(f"⚠️ Error listing models: {e}")
        return 'gemini-1.5-flash'

def generate_marketing_insights(data_summary: Dict[str, Any]) -> str:
    """
    Receives a metrics summary (JSON) and generates strategic recommendations.
    """
    try:
        # 1. Prepare the Prompt
        summary_text = str(data_summary)
        
        prompt = f"""
        Act as a Senior Digital Marketing Consultant. Analyze the following campaign performance summary:
        
        DATA:
        {summary_text}
        
        YOUR TASK:
        1. Identify the WORST performing channel (budget waste).
        2. Identify the BEST performing channel (scaling opportunity).
        3. Provide 3 specific tactical recommendations to improve global ROAS.
        
        RESPONSE FORMAT:
        Use Markdown. Be direct, professional, and data-oriented. Do not use generic phrases.
        """
        
        # 2. Auto-select Model
        model_name = get_available_model()
        print(f"🤖 Using Model: {model_name}")
        
        model = genai.GenerativeModel(model_name)
        
        # Generate content
        response = model.generate_content(prompt)
        
        if response and hasattr(response, 'text'):
            return response.text
        else:
            return "Error: The model returned an empty response."

    except Exception as e:
        return f"AI Engine Error ({type(e).__name__}): {str(e)}"