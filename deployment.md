# Zomato AI Deployment Guide

Follow these steps to deploy your full-stack AI Restaurant Recommender.

## 1. Backend Deployment (FastAPI)
Since the Streamlit URL is a UI and not an API, you should deploy the FastAPI backend to a service like **Render** or **Railway**.

1.  **Repository**: Connect your GitHub repo to **Render**.
2.  **Runtime**: Python 3.x
3.  **Build Command**: `pip install -r requirements.txt`
4.  **Start Command**: `uvicorn source.phase_5.api:app --host 0.0.0.0 --port $PORT`
5.  **Environment Variables**:
    - `GROQ_API_KEY`: (Your Groq API Key)
    - `PYTHONPATH`: `.`
    - `ALLOWED_ORIGINS`: `https://your-vercel-domain.vercel.app` (Add this AFTER deploying the frontend)

## 2. Frontend Deployment (Vercel)
1.  **Repository**: Connect the same GitHub repo to **Vercel**.
2.  **Framework Preset**: Next.js
3.  **Environment Variables**:
    - `NEXT_PUBLIC_API_URL`: Paste the URL of your deployed Render backend (e.g., `https://zomato-backend.onrender.com`).
4.  **Deploy**: Click Deploy!

## 3. Local Testing
To run the full-stack version locally:
1.  **Terminal 1 (Backend)**: `python source/phase_5/api.py`
2.  **Terminal 2 (Frontend)**: `npm run dev`
3.  Open [http://localhost:3000](http://localhost:3000)

---
*Note: Your Streamlit app at the existing URL will continue to work as a standalone "all-in-one" version, but the Vercel + FastAPI setup is the standard professional architecture.*
