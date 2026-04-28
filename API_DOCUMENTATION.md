# APIs & External Services Used in This Project

## 📋 Overview

This project uses **3 main external APIs/services** and several Python libraries.

---

## 🔑 1. Groq API (LLM Service)

**Purpose:** AI-powered restaurant recommendations using Large Language Models

### Details:
- **Service:** Groq Cloud API
- **Model Used:** `llama-3.3-70b-versatile`
- **Type:** REST API (Chat Completions)
- **Documentation:** https://console.groq.com/docs

### Where It's Used:
- **File:** `source/phase 4/src/llm_engine.py` (Lines 5, 34, 74-83)
- **Function:** `LLMRecommendationEngine.generate_recommendations()`

### API Key Location:
- **File:** `source/phase 1/.env`
- **Variable:** `GROQ_API_KEY`
- **Current Key:** `gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (Replace with your actual key in .env)

### How to Get Your Own:
1. Go to https://console.groq.com
2. Sign up for a free account
3. Navigate to API Keys section
4. Generate a new API key
5. Update the `.env` file with your key

### Usage Example:
```python
from groq import Groq

client = Groq(api_key="your_api_key")
response = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a food concierge..."},
        {"role": "user", "content": "Recommend restaurants..."}
    ],
    model="llama-3.3-70b-versatile",
    response_format={"type": "json_object"}
)
```

### Rate Limits (Free Tier):
- **Requests:** 30 requests/minute
- **Tokens:** 6,000 tokens/minute
- **Daily Limit:** 200 requests/day

---

## 📊 2. Hugging Face Datasets API

**Purpose:** Download the Zomato restaurant dataset

### Details:
- **Service:** Hugging Face Hub
- **Dataset:** `ManikaSaini/zomato-restaurant-recommendation`
- **Type:** Python Library API
- **Documentation:** https://huggingface.co/docs/datasets

### Where It's Used:
- **File:** `source/phase 2/src/data_ingestion.py` (Line 3, ~Line 30)
- **Function:** Data acquisition and loading

### How It Works:
```python
from datasets import load_dataset

# Download dataset from Hugging Face Hub
dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
```

### No API Key Required:
- Hugging Face datasets are publicly accessible
- No authentication needed for public datasets
- Automatic caching for faster subsequent loads

### Dataset Info:
- **URL:** https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation
- **Records:** 41,410 restaurants
- **Columns:** Name, Location, Cuisine, Rating, Cost, etc.

---

## 🎨 3. Streamlit Framework (Not an API, but important)

**Purpose:** Build the web UI frontend

### Details:
- **Service:** Streamlit (Open-source Python framework)
- **Type:** Web Framework
- **Documentation:** https://docs.streamlit.io

### Where It's Used:
- **File:** `source/phase 5/app.py` (Throughout the file)
- **Components:** 
  - `st.set_page_config()` - Page configuration
  - `st.sidebar` - Input controls
  - `st.text_input()`, `st.selectbox()`, `st.slider()` - UI widgets
  - `st.spinner()`, `st.success()`, `st.error()` - Status messages
  - `st.container()`, `st.columns()` - Layout

### No API Key Required:
- Completely free and open-source
- Runs locally on your machine
- No external service calls

---

## 📦 Python Libraries Used (Not APIs, but dependencies)

### Core Libraries:

| Library | Purpose | Used In |
|---------|---------|---------|
| **pandas** | Data manipulation & analysis | Phase 2, 3, 5 |
| **numpy** | Numerical operations | Phase 2, 3 |
| **pyarrow** | Parquet file support | Phase 2, 5 |
| **python-dotenv** | Environment variable management | Phase 1, 4 |

### Where to Find Them:
- **requirements.txt** files in each phase directory
- **Installed in:** `source/venv/Lib/site-packages/`

---

## 🔐 API Keys & Secrets Management

### Current Configuration:

**Groq API Key:**
```
Location: source/phase 1/.env
Format: GROQ_API_KEY=gsk_xxxxxxxxxxxxx
Status: ✅ Configured
```

### Security Best Practices:
1. ✅ `.env` file is in `.gitignore` (not committed to Git)
2. ✅ API key loaded via `python-dotenv`
3. ✅ Never hardcode keys in source code
4. ⚠️ Don't share your `.env` file publicly

### How to Update API Key:
```bash
# Open the .env file
notepad "source\phase 1\.env"

# Update the key
GROQ_API_KEY=your_new_api_key_here

# Save and restart the app
```

---

## 🌐 External Service Endpoints

### Groq API Endpoint:
```
POST https://api.groq.com/openai/v1/chat/completions
```

### Hugging Face Dataset URL:
```
https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation
```

### Streamlit App (Local):
```
http://localhost:8502
```

---

## 📊 API Usage Monitoring

### Check Groq API Usage:
1. Login to https://console.groq.com
2. Go to "Usage" or "Billing" section
3. View request count and token usage

### View Logs:
```
Phase 2: source/phase 2/logs/data_ingestion.log
Phase 3: source/phase 3/logs/search_engine.log
Phase 4: source/phase 4/logs/llm_engine.log
Phase 5: source/phase 5/logs/backend_controller.log
```

### Example Log Entry (Groq API):
```
2026-04-24 22:05:33,133 - httpx - INFO - HTTP Request: POST 
https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
```

---

## 🚀 Testing APIs

### Test Groq API:
```bash
cd "source\phase 4"
..\venv\Scripts\python.exe src\llm_engine.py
```

### Test Hugging Face Dataset:
```bash
cd "source\phase 2"
..\venv\Scripts\python.exe src\data_ingestion.py
```

### Test Complete Flow:
```bash
cd "source\phase 5"
..\venv\Scripts\python.exe tests\test_backend.py
```

---

## 💰 Cost Breakdown

| Service | Tier | Cost | Limits |
|---------|------|------|--------|
| **Groq API** | Free | $0 | 30 req/min, 200/day |
| **Hugging Face** | Free | $0 | Unlimited (public datasets) |
| **Streamlit** | Open Source | $0 | Unlimited (local) |
| **Total** | | **$0** | |

---

## 🔗 Useful Links

- **Groq Console:** https://console.groq.com
- **Groq API Docs:** https://console.groq.com/docs
- **Hugging Face:** https://huggingface.co
- **Datasets Docs:** https://huggingface.co/docs/datasets
- **Streamlit Docs:** https://docs.streamlit.io
- **Pandas Docs:** https://pandas.pydata.org/docs/
- **Project Dataset:** https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation

---

## ⚙️ Configuration Files

### Environment Variables:
```
source/phase 1/.env
├── GROQ_API_KEY (Required)
```

### Requirements:
```
source/phase 1/requirements.txt
source/phase 2/requirements.txt
source/phase 3/requirements.txt
source/phase 4/requirements.txt
source/phase 5/requirements.txt
```

---

## 📝 Summary

**APIs Requiring Keys:**
1. ✅ Groq API - For LLM recommendations (Key in `.env`)

**APIs Without Keys:**
2. ✅ Hugging Face Datasets - For data download (Public)

**Frameworks (No API):**
3. ✅ Streamlit - For web UI (Local)
4. ✅ Pandas/NumPy - For data processing (Local)

**Total External Dependencies:** 2 APIs + 4 libraries
**Total Cost:** $0 (All free tiers)
**API Keys Needed:** 1 (Groq)
