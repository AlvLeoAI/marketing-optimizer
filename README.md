🚀 AI Marketing Performance Optimizer

Turn your marketing data into actionable strategic insights using Generative AI.

This Full-Stack application ingests campaign performance data (via CSV or Real-Time Webhooks), calculates key metrics like ROAS and CPA, and uses an AI Agent (Google Gemini 1.5 Flash) to generate professional audit reports and budget allocation recommendations.

🌟 Key Features

📊 Interactive Dashboard: Visualizes spending, revenue, and efficiency trends using Streamlit and Plotly.

🤖 AI Strategic Consultant: An embedded AI agent analyzes your data patterns to identify budget waste and scaling opportunities.

⚡ Real-Time Ingestion: A dedicated Webhook endpoint designed to receive leads directly from automation tools like n8n, Make, or Zapier.

🧮 Advanced Analytics: Automated calculation of complex metrics (ROAS, Conversion Rate, CPA) using a vectorized Pandas engine.

🛡️ Data Validation: Robust data integrity checks using Pydantic schemas.

🛠️ Tech Stack

Backend: FastAPI (Python 3.10+)

Frontend: Streamlit

AI Model: Google Gemini 1.5 Flash (via google-generativeai)

Data Processing: Pandas, NumPy

Validation: Pydantic, Email-Validator

Containerization: Docker & DevContainers

🚀 Quick Start (Local Development)

1. Clone the Repository

git clone [https://github.com/AlvLeoAI/marketing-optimizer.git](https://github.com/AlvLeoAI/marketing-optimizer.git)
cd marketing-optimizer


2. Environment Setup

Create a virtual environment and install dependencies:

# Create venv
python -m venv venv

# Activate venv (Windows)
.\venv\Scripts\activate

# Activate venv (Mac/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt


3. Configuration (.env)

Create a .env file in the root directory and add your API Key:

GEMINI_API_KEY="your_google_ai_studio_key"
ENV="development"


4. Run the Application

You need to run both the Backend and Frontend terminals.

Terminal 1: Backend API

uvicorn backend.main:app --reload
# Server starts at [http://127.0.0.1:8000](http://127.0.0.1:8000)


Terminal 2: Frontend Dashboard

streamlit run frontend/app.py
# App opens at http://localhost:8501


📖 Usage Guide

A. Batch Analysis (CSV)

Go to the "Upload Data" page.

Upload a CSV file containing: date, channel, spend, revenue, clicks, conversions.

Click "Process Data with AI".

Navigate to "Dashboard" to see the charts.

Navigate to "AI Insights" to get the strategic report.

B. Real-Time Webhook (n8n / Make)

Send a POST request to ingest leads automatically:

Endpoint: POST /integrations/webhook/ingest-data

Payload Example:

{
  "source": "Facebook Ads",
  "lead_email": "new.client@example.com",
  "metadata": {
    "campaign_name": "Q3_Growth",
    "is_vip": true
  }
}


Check the "Dashboard" -> "Live Leads Feed" section to see them appear in real-time.

🧪 Testing

Run the automated test suite to ensure system stability:

# Run all tests
pytest

# Run only unit tests
pytest tests/unit

# Run frontend smoke tests
pytest frontend/tests


📂 Project Structure

marketing-optimizer/
├── backend/             # FastAPI Logic
│   ├── routers/         # API Endpoints (Analytics, AI, Integrations)
│   ├── services/        # Business Logic (Math Engine, Gemini Client)
│   └── models/          # Pydantic Schemas
├── frontend/            # Streamlit App
│   ├── pages/           # Dashboard Pages
│   ├── components/      # UI Widgets
│   └── utils/           # API Clients
├── tests/               # Pytest Suite
└── data/                # Sample Datasets


☁️ Deployment

See DEPLOYMENT.md for detailed instructions on how to deploy:

Backend: Google Cloud Run

Frontend: Streamlit Cloud

Author: AlvLeoAI
Built for the Roverpass Technical Showcase.
