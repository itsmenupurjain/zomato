# Phase 5: Frontend UI Implementation

## Overview
This phase implements a complete Streamlit-based frontend UI for the AI-Powered Restaurant Recommendation System.

## Features

### 🎨 User Interface
- **Modern, responsive design** with custom CSS styling
- **Sidebar controls** for easy input management
- **Restaurant cards** with attractive layout showing:
  - Restaurant name
  - Rating, Cost, Cuisine, Location
  - AI-generated personalized explanation

### 🔧 Input Controls
- **Location**: Text input for area/locality search
- **Budget Range**: Dropdown (Low, Medium, High, Any)
- **Preferred Cuisines**: Multi-select dropdown with 18+ cuisine options
- **Minimum Rating**: Slider (0.0 - 5.0)
- **Additional Preferences**: Text area for specific requirements

### ⚡ Performance Features
- **Backend caching** using `@st.cache_resource` to avoid reloading on each interaction
- **Loading spinner** during API calls
- **Error handling** with user-friendly messages
- **Input validation** to prevent empty searches

### 💡 User Experience
- **Welcome screen** with feature highlights
- **Example queries** to help users get started
- **Real-time feedback** with success/warning/error messages
- **Responsive layout** that works on different screen sizes

## File Structure
```
phase 5/
├── app.py                      # Streamlit frontend application
├── requirements.txt            # Python dependencies
├── run_app.bat                 # Windows launcher script
├── SETUP_GUIDE.md             # This file
├── src/
│   └── backend_controller.py  # Backend orchestration layer
├── tests/
│   └── test_backend.py        # Backend integration tests
└── logs/
    └── backend_controller.log # Application logs
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Phase 2 completed (cleaned_restaurants.parquet must exist)
- Phase 3 & 4 completed (search_engine.py and llm_engine.py)
- Valid GROQ_API_KEY in `.env` file

### Step 1: Install Dependencies

```bash
# Navigate to phase 5 directory
cd "c:\Users\Admin\Desktop\zomato project\source\phase 5"

# Activate virtual environment (if not already activated)
cd ..\..
.\venv\Scripts\activate.bat
cd "source\phase 5"

# Install requirements
pip install -r requirements.txt
```

### Step 2: Configure Environment

Ensure your `.env` file (in phase 1 directory) contains:
```
GROQ_API_KEY=your_actual_api_key_here
```

### Step 3: Run the Application

**Option 1: Using the launcher script (Recommended for Windows)**
```bash
run_app.bat
```

**Option 2: Manual execution**
```bash
# Make sure you're in the phase 5 directory
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

## Usage Guide

### Basic Search
1. Enter a location (e.g., "Indiranagar")
2. Select budget range
3. Choose preferred cuisines (optional)
4. Set minimum rating (optional)
5. Click "Find Restaurants"

### Advanced Search
1. Fill in basic filters as above
2. Add specific preferences in the text area:
   - "romantic dinner for anniversary"
   - "family-friendly with kids play area"
   - "quick lunch, good for groups"
   - "vegetarian options, outdoor seating"

### Example Searches
The app provides 3 pre-configured examples:
1. **Romantic Italian**: Medium budget, Indiranagar, 4.0+ rating
2. **Casual Cafe**: Low budget, Koramangala, Fast Food & Cafe
3. **Fine Dining**: High budget, Japanese/Thai, 4.5+ rating

## Technical Details

### Backend Integration
- **Data Flow**: UI → BackendController → SearchEngine → LLMEngine → UI
- **Caching**: Backend controller is cached using Streamlit's `@st.cache_resource`
- **Error Handling**: Graceful handling of:
  - Missing data files
  - API failures
  - Empty results
  - Invalid inputs

### UI Components
- **st.set_page_config**: Custom page title, icon, and layout
- **st.sidebar**: Input controls panel
- **st.container**: Restaurant card containers
- **st.spinner**: Loading indicator
- **st.success/warning/error**: User feedback messages
- **st.expander**: Example query details

### Custom Styling
- Restaurant cards with colored left border
- Meta information badges (rating, cost, cuisine, location)
- Explanation box with highlighted background
- Responsive flex layout for metadata

## Troubleshooting

### Issue: "Data file not found"
**Solution**: Ensure Phase 2 has been completed and `cleaned_restaurants.parquet` exists in `phase 2/data/`

### Issue: "GROQ_API_KEY is not set"
**Solution**: Add your API key to `phase 1/.env` file:
```
GROQ_API_KEY=gsk_your_actual_key
```

### Issue: "Module not found" errors
**Solution**: Verify all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: App won't start
**Solution**: Check if Streamlit is properly installed:
```bash
python -m streamlit --version
```

## Testing

Run backend integration tests:
```bash
python tests/test_backend.py
```

This will test:
1. Normal search with user query
2. Auto-generated query (empty input)
3. Impossible constraints (edge case)

## Performance Tips

1. **First Load**: The initial load may take a few seconds as the parquet file is read
2. **Subsequent Searches**: Backend is cached, so only LLM API call adds latency
3. **API Rate Limits**: Groq has rate limits; avoid rapid consecutive searches

## Next Steps (Phase 6)
- Unit testing for data cleaning functions
- Prompt tuning and guardrails
- Performance optimization with `@st.cache_data`
- Edge case testing for LLM responses

## Support
For issues or questions, check:
- Application logs in `logs/backend_controller.log`
- Streamlit documentation: https://docs.streamlit.io
- Groq API documentation: https://console.groq.com/docs
