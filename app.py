import streamlit as st
import os
import sys
import pandas as pd
from PIL import Image

# Add current directory to path to import local modules
sys.path.append(os.path.join(os.getcwd(), "source", "phase_5", "src"))
from backend_controller import BackendController

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Zomato AI | Premium Concierge",
    page_icon="🍴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS (GLASSMORPHISM) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #1e1e1e, #000000);
        color: white;
    }
    
    /* Glass Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 1.5rem;
    }
    
    .restaurant-card {
        border-radius: 32px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: transform 0.3s ease;
    }
    
    .restaurant-card:hover {
        transform: translateY(-5px);
        border-color: #ff3e3e;
    }
    
    .premium-text {
        background: linear-gradient(90deg, #ff3e3e, #ff8e8e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #ff3e3e, #d32f2f);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.8rem 2rem;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        box-shadow: 0 4px 20px rgba(255, 62, 62, 0.4);
        transform: scale(1.02);
    }
    
    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE BACKEND ---
@st.cache_resource
def get_controller():
    # Possible relative paths to the data file
    possible_paths = [
        os.path.join("source", "phase_2", "data", "cleaned_restaurants.parquet"),
        os.path.join("zomato", "source", "phase_2", "data", "cleaned_restaurants.parquet"),
        "cleaned_restaurants.parquet" # Fallback if moved to root
    ]
    
    data_path = None
    for p in possible_paths:
        if os.path.exists(p):
            data_path = p
            break
            
    if not data_path:
        # Final attempt: Absolute path check
        current_dir = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(current_dir, "source", "phase_2", "data", "cleaned_restaurants.parquet")
        if os.path.exists(abs_path):
            data_path = abs_path
            
    if not data_path:
        st.error("🚨 Critical Error: Restaurant database not found. Please ensure 'cleaned_restaurants.parquet' is in 'source/phase_2/data/'.")
        st.info("Tip: If you are using Git LFS, ensure the file was pushed correctly.")
        return None
        
    return BackendController(data_path)

controller = get_controller()

# --- IMAGE SYSTEM ---
def get_unique_image(cuisine_str, name_str):
    cuisine_pools = {
        "italian": ["https://images.unsplash.com/photo-1551183053-bf91a1d81141", "https://images.unsplash.com/photo-1546549032-9571cd6b27df", "https://images.unsplash.com/photo-1574071318508-1cdbad80ad38"],
        "chinese": ["https://images.unsplash.com/photo-1552611052-33e04de081de", "https://images.unsplash.com/photo-1585032226651-759b368d7246"],
        "north indian": ["https://images.unsplash.com/photo-1585937421612-70a0f2455f75", "https://images.unsplash.com/photo-1565557623262-b51c2513a641"],
        "cafe": ["https://images.unsplash.com/photo-1509042239860-f550ce710b93", "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085"],
        "desserts": ["https://images.unsplash.com/photo-1551024601-bec78aea704b", "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e"],
        "default": ["https://images.unsplash.com/photo-1517248135467-4c7edcad34c4", "https://images.unsplash.com/photo-1552566626-52f8b828add9"]
    }
    
    cuisine_str = cuisine_str.lower()
    name_hash = sum(ord(c) for c in name_str)
    
    selected_pool = cuisine_pools["default"]
    for key in cuisine_pools:
        if key in cuisine_str:
            selected_pool = cuisine_pools[key]
            break
            
    base_url = selected_pool[name_hash % len(selected_pool)]
    return f"{base_url}?auto=format&fit=crop&q=80&w=800"

# --- MAIN UI ---
def main():
    # Header
    st.markdown('<h1 style="font-size: 4rem; margin-bottom: 0;">Zomato <span class="premium-text">AI</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: rgba(255,255,255,0.4); margin-bottom: 3rem;">Your personal food concierge, powered by intelligence.</p>', unsafe_allow_html=True)

    # Search Section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Where are you?")
        locations = controller.search_engine.get_available_locations()
        location = st.selectbox("Location", ["Any"] + locations, label_visibility="collapsed")
        
        st.subheader("Maximum Budget")
        budget = st.slider("Budget (₹)", 200, 5000, 1500, step=100)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Cuisines")
        all_cuisines = ["North Indian", "Chinese", "Italian", "Street Food", "Cafe", "Desserts"]
        selected_cuisines = st.multiselect("Pick your favorites", all_cuisines)
        
        st.subheader("Ambiance & Vibes")
        ambiance = st.text_input("e.g. Romantic rooftop, Family friendly", placeholder="Tell AI what you're feeling...")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Explore Recommendations"):
        with st.spinner("Analyzing gems..."):
            results = controller.get_recommendations(
                location=location if location != "Any" else "",
                max_budget=budget,
                cuisines=selected_cuisines,
                min_rating=4.0,
                user_query=ambiance
            )
            
            if not results:
                st.error("No results found! Try loosening your filters (e.g. increasing Maximum Budget).")
            else:
                st.markdown(f"### Top {len(results)} Picks For You")
                
                for i, res in enumerate(results):
                    img_url = get_unique_image(res.get("Cuisine", ""), res.get("Name", ""))
                    
                    with st.container():
                        st.markdown(f'''
                            <div class="restaurant-card" style="margin-bottom: 2rem;">
                                <img src="{img_url}" style="width: 100%; height: 250px; object-fit: crop; border-radius: 32px 32px 0 0;">
                                <div style="padding: 2rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                                        <h2 style="margin: 0; font-weight: 900;">{res.get("Name")}</h2>
                                        <span style="background: #ff3e3e; padding: 4px 12px; border-radius: 100px; font-weight: bold; font-size: 0.8rem;">{res.get("Rating")} ⭐</span>
                                    </div>
                                    <p style="color: #ff3e3e; font-weight: bold; font-size: 0.9rem; margin-bottom: 0.5rem;">{res.get("Cuisine")}</p>
                                    <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">📍 {res.get("Location")} | 💰 ₹{res.get("Cost")} per person</p>
                                    <hr style="border-color: rgba(255,255,255,0.05); margin: 1.5rem 0;">
                                    <p style="line-height: 1.6; color: rgba(255,255,255,0.9); font-style: italic;">"{res.get("Explanation")}"</p>
                                </div>
                            </div>
                        ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
