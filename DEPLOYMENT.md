# Deployment Guide 🚀

This guide outlines the steps to deploy the AI Marketing Optimizer to a production environment. The architecture follows a decoupled pattern:

- **Backend (API):** Deployed as a Serverless Container on Google Cloud Run.
- **Frontend (UI):** Deployed on Streamlit Cloud (or any static/app hosting).

---

## 🏗️ Part 1: Backend Deployment (Google Cloud Run)

We use Google Cloud Run because it scales automatically (scale-to-zero) and supports Docker containers natively.

### Prerequisites

- Google Cloud Platform (GCP) Account.
- Google Cloud CLI installed (`gcloud`).
- Docker installed (optional, but recommended for local testing).

### Steps

#### 1. Initialize Google Cloud CLI

Login to your account and select your project:
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### 2. Enable Services

Ensure Cloud Run and Container Registry APIs are enabled:
```bash
gcloud services enable run.googleapis.com containerregistry.googleapis.com
```

#### 3. Deploy to Cloud Run

Run the following command from the project root. This builds the Docker image and deploys it in one go.
```bash
gcloud run deploy ai-marketing-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

- `--source .`: Uses the Dockerfile in the current directory.
- `--allow-unauthenticated`: Makes the API public (necessary for the Frontend to access it).

#### 4. Set Environment Variables

Once deployed, you need to configure your secrets (API Keys) in the Cloud Run dashboard or via CLI:
```bash
gcloud run services update ai-marketing-backend \
  --set-env-vars GEMINI_API_KEY="your_actual_api_key"
```

#### 5. Get the Backend URL

After successful deployment, Google will provide a URL (e.g., `https://ai-marketing-backend-xyz.a.run.app`). **Copy this URL.** You will need it for the Frontend.

---

## 🎨 Part 2: Frontend Deployment (Streamlit Cloud)

Streamlit Cloud is the easiest way to host the dashboard directly from your GitHub repository.

### Steps

#### 1. Push Code to GitHub

Ensure your project is in a public (or private) GitHub repository.

#### 2. Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Click "New App".
3. Select your repository, branch (`main`), and the main file path: `frontend/app.py`.

#### 3. Configure Backend Connection

Before clicking "Deploy", go to the **"Advanced Settings" → "Secrets"** section (or wait until it deploys and go to Settings).

You need to tell the Frontend where the Backend lives. Add this to your Streamlit Secrets:
```toml
[general]
API_BASE_URL = "https://ai-marketing-backend-xyz.a.run.app"
```

*(Replace the URL with the one you got from Google Cloud Run).*

> **Note:** You will need to update `frontend/utils/api_client.py` to read this secret instead of localhost if you haven't already.
>
> Example:
> ```python
> API_BASE_URL = st.secrets.get("general", {}).get("API_BASE_URL", "http://127.0.0.1:8000")
> ```

#### 4. Deploy!

Click "Deploy". Streamlit will install the dependencies from `requirements.txt` and launch the app.

---

## 🔄 CI/CD Pipeline (Optional - Advanced)

For automated deployments, you can set up a GitHub Action.

Create a file at `.github/workflows/deploy.yml`:
```yaml
name: Build and Deploy to Cloud Run

on:
  push:
    branches: [ "main" ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Google Auth
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - name: Deploy to Cloud Run
        uses: google-github-actions/deploy-cloudrun@v1
        with:
          service: ai-marketing-backend
          region: us-central1
          source: .
```

---

## 🛠️ Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| **503 Service Unavailable** | Backend container crashed on startup | Check Cloud Run logs. Common cause: Missing `requirements.txt` packages or invalid `.env` variables. |
| **Frontend cannot connect** | URL misconfiguration or CORS issue | Ensure the Backend URL in Streamlit Secrets does not have a trailing slash (`/`) unless your code expects it, and that the Backend allows CORS from the Streamlit domain. |
