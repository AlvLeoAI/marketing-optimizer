AI Marketing Performance Optimizer - System Architecture

1. High-Level Overview

The system follows a Decoupled Architecture pattern, separating the user interface (Frontend) from the business logic and data processing (Backend). This design ensures scalability, maintainability, and allows for independent deployment of components.

The core functionality revolves around ingesting marketing data (via CSV or Webhooks), processing it with Pandas, and using a Generative AI Agent (Google Gemini) to provide strategic insights.

graph TD
    User[User / Marketer] -->|Interacts via Browser| FE[Frontend (Streamlit)]
    External[External Automation (n8n/Make)] -->|Webhook POST| API
    
    subgraph "Client Layer"
        FE
    end

    subgraph "Server Layer (Backend API)"
        FE -->|HTTP Requests (JSON)| API[FastAPI Gateway]
        API -->|Data Processing| Engine[Analytics Engine (Pandas)]
        API -->|Inference Request| Agent[AI Agent Service]
        API -->|Ingestion| Webhook[Integration Router]
    end

    subgraph "External Services"
        Agent -->|Context & Prompt| LLM[Google Gemini Pro]
        LLM -->|Strategic Insights| Agent
    end


2. Technical Stack

Component

Technology

Description

Frontend

Streamlit

Python-based framework for rapid data dashboarding. Handles UI state and visualization.

Backend

FastAPI

High-performance, asynchronous web framework. Manages API endpoints and validation.

Data Processing

Pandas + NumPy

Vectorized data manipulation for calculating metrics like ROAS, CPA, and CR.

AI Model

Google Gemini 1.5 Flash

Generative AI model used for analyzing data patterns and generating natural language reports.

Validation

Pydantic

Data validation and settings management. Ensures data integrity for CSVs and Webhooks.

Visualization

Plotly

Interactive charting library used in the frontend.

3. Project Structure & Modules

The project is organized as a monorepo containing both the backend API and the frontend dashboard.

📂 backend/

The core logic of the application.

main.py: The entry point of the API. Configures CORS and registers routers.

routers/: Handles HTTP requests and routing.

data_analytics.py: Endpoints for file upload and metric calculation.

recommendations.py: Endpoints for AI report generation.

integrations.py: Webhook endpoints for real-time data ingestion (n8n/Make).

services/: Business logic layer.

metrics_engine.py: Pure functions for calculating marketing KPIs using Pandas.

ai_agent.py: Manages the connection with Google Gemini and prompt engineering.

models/: Pydantic schemas defining input/output data structures (The Contract).

📂 frontend/

The presentation layer.

app.py: The main entry point for the Streamlit application.

pages/: Modular pages for navigation (Upload Data, Dashboard, AI Insights).

utils/: Helper functions, specifically the API Client (api_client.py) which handles communication with the Backend.

assets/: Custom CSS styling.

4. Data Flow

Scenario A: Batch Analysis (CSV Upload)

User uploads a CSV file via the Streamlit interface.

Frontend sends the file to POST /analytics/upload-csv.

Backend validates the file structure using Pydantic models.

metrics_engine processes the data using Pandas to calculate ROAS, Total Spend, and Revenue.

Backend returns a JSON summary to the Frontend.

Frontend stores the result in st.session_state and renders interactive charts.

Scenario B: AI Consultation

User clicks "Generate AI Report" on the frontend.

Frontend sends the calculated metrics summary to POST /ai/generate-insights.

ai_agent constructs a context-aware prompt and sends it to Google Gemini.

Gemini returns a markdown-formatted strategic analysis.

Frontend displays the report to the user.

Scenario C: Real-Time Ingestion (Webhook)

An external tool (e.g., n8n) sends a JSON payload to POST /integrations/webhook/ingest-data.

Backend validates the payload (including email validation).

Data is processed/logged (simulated in-memory storage for MVP).

Dashboard updates the "Live Feed" section by polling the backend.

5. Scalability & Future Roadmap

Database: Currently using in-memory processing for speed. Future versions will implement PostgreSQL (via SQLAlchemy) for persistent data storage.

Authentication: Implementation of JWT Authentication to support multi-tenancy.

Async Processing: For large datasets, the AI analysis can be moved to a background task using Celery and Redis.