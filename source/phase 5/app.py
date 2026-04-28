import streamlit as st
import sys
import os

# Add Phase 5 src to path
phase5_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if phase5_src not in sys.path:
    sys.path.append(phase5_src)

from backend_controller import BackendController

# Page configuration
st.set_page_config(
    page_title="AI Restaurant Recommender",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stSidebar {
        background-color: #ffffff;
    }
    .restaurant-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 4px solid #ff6b6b;
    }
    .restaurant-name {
        font-size: 1.5em;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .restaurant-meta {
        display: flex;
        gap: 15px;
        margin-bottom: 15px;
        flex-wrap: wrap;
    }
    .meta-item {
        background-color: #f0f0f0;
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 0.9em;
        color: #555;
    }
    .explanation {
        background-color: #fff5f5;
        padding: 15px;
        border-radius: 8px;
        border-left: 3px solid #ff6b6b;
        font-style: italic;
        color: #444;
    }
    .header-title {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 10px;
    }
    .header-subtitle {
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_backend():
    """Load the backend controller (cached to avoid reloading on each interaction)"""
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        "phase 2", 
        "data", 
        "cleaned_restaurants.parquet"
    )
    
    if not os.path.exists(data_path):
        st.error(f"Data file not found at {data_path}. Please run Phase 2 data ingestion first.")
        return None
    
    try:
        controller = BackendController(data_path)
        return controller
    except Exception as e:
        st.error(f"Failed to initialize backend: {str(e)}")
        return None

@st.cache_data
def get_location_options(_backend):
    """Get unique location options from the database (cached)"""
    try:
        locations = _backend.search_engine.get_available_locations()
        return ["Any"] + locations
    except Exception as e:
        st.error(f"Failed to load locations: {str(e)}")
        return ["Any"]

def main():
    # Header
    st.markdown('<h1 class="header-title">🍽️ AI-Powered Restaurant Recommender</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">Discover perfect dining experiences tailored to your preferences</p>', unsafe_allow_html=True)
    
    # Initialize backend
    backend = load_backend()
    
    if backend is None:
        st.stop()
    
    # Get location options from database
    location_options = get_location_options(backend)
    
    # Sidebar - Input Controls
    with st.sidebar:
        st.header("🎯 Your Preferences")
        st.markdown("---")
        
        # Location dropdown (instead of text input)
        location = st.selectbox(
            "📍 Location",
            options=location_options,
            index=0,  # Default to "Any"
            help="Select your preferred area or locality from the database"
        )
        location = None if location == "Any" else location
        
        # Maximum Budget input (numeric)
        max_budget = st.number_input(
            "💰 Maximum Budget (₹ per person)",
            min_value=0,
            max_value=5000,
            value=0,
            step=50,
            help="Enter your maximum budget per person in INR (₹). Leave at 0 for no budget filter."
        )
        max_budget = None if max_budget == 0 else max_budget
        
        # Cuisine selection
        cuisine_options = [
            "Italian", "Chinese", "Indian", "Mexican", "Japanese", 
            "Thai", "American", "Cafe", "Fast Food", "Continental",
            "South Indian", "North Indian", "Pizza", "Burger", 
            "Desserts", "Beverages", "Seafood", "BBQ"
        ]
        
        cuisines = st.multiselect(
            "🍕 Preferred Cuisines",
            options=cuisine_options,
            default=[],
            help="Select one or more cuisines (optional)"
        )
        
        # Rating slider
        min_rating = st.slider(
            "⭐ Minimum Rating",
            min_value=0.0,
            max_value=5.0,
            value=0.0,
            step=0.1,
            help="Minimum restaurant rating (0-5)"
        )
        min_rating = None if min_rating == 0.0 else min_rating
        
        # Additional preferences
        st.markdown("---")
        st.subheader("💭 Additional Preferences")
        user_query = st.text_area(
            "Tell us more about what you're looking for",
            placeholder="e.g., romantic dinner, family-friendly, quick bite, good for groups...",
            height=100,
            help="Any specific requirements or occasion details"
        )
        
        st.markdown("---")
        
        # Search button
        search_clicked = st.button(
            "🔍 Find Restaurants",
            type="primary",
            use_container_width=True
        )
    
    # Main content area
    if search_clicked:
        # Validate inputs
        if not location and not cuisines and not user_query:
            st.warning("⚠️ Please provide at least one preference (location, cuisine, or additional details)")
        else:
            with st.spinner("🤖 AI is finding the perfect restaurants for you..."):
                try:
                    # Get recommendations from backend
                    recommendations = backend.get_recommendations(
                        location=location if location else "",
                        max_budget=max_budget,
                        cuisines=cuisines if cuisines else [],
                        min_rating=min_rating if min_rating else 0.0,
                        user_query=user_query if user_query else ""
                    )
                    
                    if len(recommendations) == 0:
                        st.warning("😔 No restaurants found matching your criteria.")
                        st.info("💡 **Try these suggestions:**\n"
                               "• Widen your location selection\n"
                               "• Increase your maximum budget\n"
                               "• Select fewer cuisine filters\n"
                               "• Lower the minimum rating requirement")
                    elif len(recommendations) < 3:
                        st.warning(f"⚠️ Only found {len(recommendations)} restaurant(s) matching your criteria.")
                        st.info("💡 **For more options, try:**\n"
                               "• Widen your location selection\n"
                               "• Increase your maximum budget\n"
                               "• Select fewer cuisine filters\n"
                               "• Lower the minimum rating requirement")
                        st.markdown("---")
                        # Display the limited recommendations
                        for idx, rec in enumerate(recommendations, 1):
                            with st.container():
                                st.markdown(f"""
                                    <div class="restaurant-card">
                                        <div class="restaurant-name">{idx}. {rec.get('Name', 'Unknown Restaurant')}</div>
                                        <div class="restaurant-meta">
                                            <span class="meta-item">⭐ {rec.get('Rating', 'N/A')}</span>
                                            <span class="meta-item">💵 ₹{rec.get('Cost', 'N/A')} for two</span>
                                            <span class="meta-item">🍽️ {rec.get('Cuisine', 'N/A')}</span>
                                            <span class="meta-item">📍 {rec.get('Location', 'N/A')}</span>
                                        </div>
                                        <div class="explanation">
                                            <strong>Why we recommend this:</strong><br>
                                            {rec.get('Explanation', 'No explanation available')}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.success(f"✨ Found {len(recommendations)} perfect matches for you!")
                        st.markdown("---")
                        
                        # Display recommendations in cards
                        for idx, rec in enumerate(recommendations, 1):
                            with st.container():
                                st.markdown(f"""
                                    <div class="restaurant-card">
                                        <div class="restaurant-name">{idx}. {rec.get('Name', 'Unknown Restaurant')}</div>
                                        <div class="restaurant-meta">
                                            <span class="meta-item">⭐ {rec.get('Rating', 'N/A')}</span>
                                            <span class="meta-item">💵 ₹{rec.get('Cost', 'N/A')} for two</span>
                                            <span class="meta-item">🍽️ {rec.get('Cuisine', 'N/A')}</span>
                                            <span class="meta-item">📍 {rec.get('Location', 'N/A')}</span>
                                        </div>
                                        <div class="explanation">
                                            <strong>Why we recommend this:</strong><br>
                                            {rec.get('Explanation', 'No explanation available')}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    st.exception(e)
    
    else:
        # Welcome message when no search has been performed
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                ### 🎯 Smart Filtering
                Specify your location, budget, and cuisine preferences to narrow down the best options.
            """)
        
        with col2:
            st.markdown("""
                ### 🤖 AI-Powered
                Our LLM engine analyzes your preferences and provides personalized recommendations.
            """)
        
        with col3:
            st.markdown("""
                ### 💡 Contextual Insights
                Get detailed explanations for why each restaurant matches your specific needs.
            """)
        
        st.markdown("---")
        
        # Example queries
        st.markdown("### 💡 Try These Example Searches:")
        
        example_queries = [
            {
                "location": "Indiranagar",
                "budget": "Medium",
                "cuisines": ["Italian"],
                "min_rating": 4.0,
                "query": "Looking for a romantic place for anniversary dinner"
            },
            {
                "location": "Koramangala",
                "budget": "Low",
                "cuisines": ["Fast Food", "Cafe"],
                "min_rating": 3.5,
                "query": "Quick bite with friends, good ambiance"
            },
            {
                "location": "",
                "budget": "High",
                "cuisines": ["Japanese", "Thai"],
                "min_rating": 4.5,
                "query": "Fine dining experience for family celebration"
            }
        ]
        
        for i, example in enumerate(example_queries, 1):
            with st.expander(f"Example {i}: {example['query'][:50]}..."):
                st.write(f"**Location:** {example['location'] or 'Any'}")
                st.write(f"**Budget:** {example['budget']}")
                st.write(f"**Cuisines:** {', '.join(example['cuisines'])}")
                st.write(f"**Min Rating:** {example['min_rating']}")
                st.write(f"**Query:** {example['query']}")
                
                if st.button(f"Use Example {i}", key=f"example_{i}"):
                    # Set session state for example (would need additional logic to auto-fill)
                    st.info("Adjust the sidebar filters to match this example and click 'Find Restaurants'!")

if __name__ == "__main__":
    main()
