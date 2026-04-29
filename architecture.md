# Architecture & Development Phases
**AI-Powered Restaurant Recommendation System (Zomato Use Case)**

## Overview
This document outlines the detailed step-by-step architecture for building an AI-powered restaurant recommendation service, leveraging structured data and Large Language Models (LLMs).

## phase_7: Resilience & Error Handling
1.  **Scenario: LLM Failure (API/Parsing Error)**
    - **Behavior:** If the Groq API fails or returns invalid JSON, the `BackendController` catches the exception.
    - **Fix:** Bypasses the LLM and uses the `Fallback Engine` to serve the top-rated restaurants from the pre-filtered structured data.
2.  **Scenario: No Matching Data (Zero Results)**
    - **Behavior:** If strict filters (Location + Budget + Cuisine + Rating) return zero rows.
    - **Fix:** Implements a **Tiered Relaxation** strategy. It automatically attempts a second "Relaxed Search" by increasing the budget range (+50%) and ignoring the rating threshold before returning an empty state.
3.  **Scenario: Total Database Absence**
    - **Behavior:** When even relaxed filters return nothing.
    - **Fix:** Frontend triggers a guided "Empty State" UI that asks the user to manually loosen their search criteria.

---

## phase_1: Project Setup & Environment Preparation
1. **Repository Setup:** 
   - Initialize the project directory and set up Git version control.
   - Create a structured project layout (e.g., `data/`, `src/`, `notebooks/`, `tests/`).
2. **Virtual Environment & Dependencies:** 
   - Create an isolated Python virtual environment (e.g., using `venv` or `conda`).
   - Create a `requirements.txt` and install necessary libraries: 
     - `pandas` (Data manipulation)
     - `datasets` (Fetching from Hugging Face)
     - `groq` (LLM API client)
     - `python-dotenv` (Environment variable management)
     - `fastapi` (Backend API framework)
     - `uvicorn` (ASGI server)
     - `next` (Frontend React framework)
3. **Environment Variables:** 
   - Create a `.env` file to securely store credentials like `GROQ_API_KEY`.
   - Add `.env` to `.gitignore` to prevent exposing secrets.
4. **Logging Setup:** 
   - Configure basic Python logging to track application events, errors, and LLM API latencies.

## phase_2: Data Ingestion & Preprocessing
1. **Data Acquisition:** 
   - Use the `datasets` library to download `ManikaSaini/zomato-restaurant-recommendation` from the Hugging Face hub.
   - Convert the Hugging Face dataset object into a Pandas DataFrame for easier manipulation.
2. **Data Cleaning & Transformation:** 
   - **Missing Values:** Identify and handle missing or null values in critical columns (Name, Location, Cuisine, Rating).
   - **Data Normalization:** 
     - Parse cost strings (e.g., "₹500 for two") into numeric integer values representing cost per person.
     - Convert comma-separated cuisine strings into clean lists.
     - Standardize location strings to ensure consistent filtering.
     - Convert rating strings into float values.
3. **Structured Storage:** 
   - Export the cleaned DataFrame into a `.parquet` file in the `data/` directory. Parquet is highly optimized for fast read speeds and takes up less disk space compared to CSV, making it ideal for loading into a Streamlit app.

## phase_3: Search & Integration Layer
1. **Preference Collection Schema:** 
   - Map user inputs to data columns:
     - **Location:** Dropdown selection from database locations (or "Any" for no filter).
     - **Maximum Budget:** User-defined numerical maximum cost per person (filters restaurants with cost <= max_budget).
     - **Cuisine:** List intersection (check if user cuisine exists in restaurant cuisine list).
     - **Rating:** Numerical threshold (`>= min_rating`).
2. **Filtering Engine:** 
   - Implement a Python function that takes the user preferences and applies boolean masks to the Pandas DataFrame.
   - Ensure the function returns a manageable subset of matching restaurants (e.g., top 10-20 sorted by rating) to act as a pre-filter. This is crucial for staying within the LLM's maximum context window and reducing token costs.
3. **Location Data Service:**
   - Implement a method to extract and return all unique locations from the database.
   - Return sorted list of locations for use in frontend dropdown component.
4. **Context Generation:** 
   - Transform the pre-filtered dataframe rows into a concise string or JSON block. 
   - Example format per restaurant: `Name: {name}, Cuisine: {cuisine}, Rating: {rating}, Cost: {cost}, Location: {location}`.

## phase_4: LLM Recommendation Engine
1. **Prompt Engineering:** 
   - **System Prompt:** Define the LLM's persona as an expert food concierge. Establish rules (e.g., "Only recommend restaurants from the provided context", "Keep explanations concise").
   - **User Prompt:** Inject the user's raw query (e.g., "Looking for a family-friendly Italian place") alongside the structured context block generated in phase_3.
2. **LLM Invocation:** 
   - Initialize the Groq API client.
   - Send the prompt to a fast model (e.g., `llama3-70b-8192` or `mixtral-8x7b-32768`) to ensure low-latency responses suitable for a real-time UI.
3. **Reasoning & Ranking:** 
   - Instruct the LLM to evaluate the pre-filtered options against the user's specific nuances, select exactly 3-5 best fits, and generate a unique, compelling, human-like explanation for each choice.
4. **Response Parsing:** 
   - Prompt the LLM to return its response in a structured format (like JSON or specific Markdown headers).
   - Parse the LLM output in Python to separate the restaurant details from the generated explanations for clean UI rendering.

## phase_5: Backend & UI Integration
1. **Backend Controller Development:**
   - Develop a unified controller class (`backend_controller.py`) that orchestrates the flow between the Data Filtering Engine and the LLM Recommendation Engine.
   - Combine the structured filtering output (Rating, Cost, Cuisine) with the LLM's unstructured explanations to create a clean, unified data model for the frontend.
2. **Framework Integration (Frontend):** 
   - Initialize a Streamlit application (`app.py`).
3. **Input Components (Sidebar/Main):** 
   - Create interactive widgets:
     - `st.selectbox` for Location (populated from database).
     - `st.number_input` for Maximum Budget (user enters numeric value in INR).
     - `st.multiselect` for Cuisines.
     - `st.slider` for Minimum Rating.
     - `st.text_area` for additional text constraints (e.g., "romantic", "fast service").
4. **Result Presentation:** 
   - Add a "Find Restaurants" button.
   - Show a loading spinner (`st.spinner`) while the data filtering and LLM API call are in progress.
   - Display the final recommendations using `st.columns` or `st.container` to create visual "cards".
   - Each card should clearly show the Restaurant Name, Rating, Cost, Cuisine, and crucially, the AI-generated personalized explanation.
5. **Empty State Handling:**
    - If the stored data contains zero matching restaurants, display a clear message asking the user to loosen their search criteria (e.g., increase budget or expand location).

## phase_6: Testing & Optimization
1. **Unit Testing:** 
   - Write tests using `pytest` to ensure data cleaning functions work correctly (e.g., parsing costs properly) and the filtering logic correctly applies masks without dropping valid results.
2. **Prompt Tuning & Guardrails:** 
   - Test the LLM with edge-case queries to ensure it doesn't hallucinate restaurants not provided in the context.
   - Adjust system instructions if the generated text is too long or misses the user's specific constraints.
3. **Performance Optimization:** 
   - Use Streamlit's `@st.cache_data` decorator on the function that loads the Parquet file. This ensures the dataset is only read from disk once when the app starts, drastically reducing latency for user queries.
   - Optimize Groq API calls by only passing the strictly necessary fields in the context string.
