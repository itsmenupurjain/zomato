import sys
import os
import logging
import pandas as pd
import numpy as np

# Setup logging - Cloud-Native approach
is_vercel = os.getenv("VERCEL") == "1"
handlers = [logging.StreamHandler(sys.stdout)]

if not is_vercel:
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    handlers.append(logging.FileHandler(os.path.join(log_dir, "backend_controller.log")))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=handlers
)
logger = logging.getLogger("backend_controller")

# Add phase_3 and phase_4 paths to sys.path to import engines
source_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
phase3_src = os.path.join(source_dir, "phase_3", "src")
phase4_src = os.path.join(source_dir, "phase_4", "src")

if phase3_src not in sys.path: sys.path.append(phase3_src)
if phase4_src not in sys.path: sys.path.append(phase4_src)

try:
    from search_engine import RestaurantSearchEngine
    from llm_engine import LLMRecommendationEngine
except ImportError as e:
    logger.error(f"Failed to import required engines: {e}")
    raise

class BackendController:
    def __init__(self, data_path: str):
        self.search_engine = RestaurantSearchEngine(data_path)
        self.llm_engine = LLMRecommendationEngine()

    def get_recommendations(self, location: str, max_budget: float, cuisines: list, min_rating: float, user_query: str):
        logger.info(f"Processing request: Location={location}, Max Budget={max_budget}, Cuisines={cuisines}, Rating>={min_rating}")
        
        # 1. Filter Data (Search Engine phase_3) - Strict Match
        filtered_df = self.search_engine.filter_restaurants(
            location=location,
            max_budget=max_budget,
            cuisines=cuisines,
            min_rating=min_rating,
            top_k=5
        )
        
        # Scenario: No Data in Strict Filter -> Try Relaxed Match (Ignore rating and slightly increase budget)
        if filtered_df.empty:
            logger.info("No strict matches found. Attempting Relaxed Search...")
            filtered_df = self.search_engine.filter_restaurants(
                location=location,
                max_budget=max_budget * 1.5 if max_budget else None,
                cuisines=cuisines,
                min_rating=None, # Relax rating
                top_k=5
            )
        
        if filtered_df.empty:
            logger.info("Even relaxed search returned 0 results. Triggering Zero Data state.")
            return []

        # 2. Generate Context Block
        context_block = self.search_engine.generate_context(filtered_df)
        
        # 3. Get LLM Recommendations (LLM Engine phase_4)
        if not user_query or user_query.strip() == "":
            cuisine_str = ", ".join(cuisines) if cuisines else "various"
            budget_str = f"maximum budget of ₹{max_budget}" if max_budget else "flexible budget"
            user_query = f"I am looking for {cuisine_str} food in {location or 'the city'} with a {budget_str}."
            
        llm_results = self.llm_engine.generate_recommendations(user_query, context_block)
        
        # 4. Combine LLM output with structured data (ensure NO duplicates)
        final_results = []
        seen_names = set()  # Track restaurant names to prevent duplicates
        
        for rec in llm_results:
            rec_name = rec.get("name")
            explanation = rec.get("explanation")
            
            # Skip if this restaurant was already added
            if rec_name and str(rec_name).lower() in seen_names:
                logger.warning(f"Skipping duplicate recommendation: {rec_name}")
                continue
            
            # Find the matching structured data (case insensitive)
            match = filtered_df[filtered_df['Name'].str.lower() == str(rec_name).lower()]
            if not match.empty:
                row = match.iloc[0]
                cuisine_val = row.get('Cuisine', [])
                cuisine_str = ", ".join(cuisine_val) if isinstance(cuisine_val, (list, tuple, np.ndarray)) else str(cuisine_val)
                
                final_results.append({
                    "Name": row.get("Name"),
                    "Rating": row.get("Rating"),
                    "Cost": row.get("Cost"),
                    "Cuisine": cuisine_str,
                    "Location": row.get("Location"),
                    "Explanation": explanation
                })
                seen_names.add(str(rec_name).lower())
            else:
                logger.warning(f"LLM recommended {rec_name} but it wasn't found in the filtered dataframe.")
                # Only add if not already in results
                if rec_name and str(rec_name).lower() not in seen_names:
                    final_results.append({
                        "Name": rec_name,
                        "Explanation": explanation,
                        "Rating": "N/A",
                        "Cost": "N/A",
                        "Cuisine": "N/A",
                        "Location": "N/A"
                    })
                    seen_names.add(str(rec_name).lower())
        
        # 5. Fallback: If we have fewer than 5 recommendations, add top-rated restaurants from filtered results
        # We ensure exactly 5 results as long as data exists in the database
        if len(final_results) < 5 and len(filtered_df) > 0:
            logger.info(f"LLM returned {len(final_results)} recommendations. Adding fallback recommendations to reach exactly 5.")
            
            # Add top-rated restaurants that weren't recommended by LLM or were missed
            for _, row in filtered_df.iterrows():
                if len(final_results) >= 5: 
                    break
                    
                row_name = str(row.get("Name", ""))
                if row_name.lower() not in seen_names:
                    cuisine_val = row.get('Cuisine', [])
                    cuisine_str = ", ".join(cuisine_val) if isinstance(cuisine_val, (list, tuple, np.ndarray)) else str(cuisine_val)
                    
                    final_results.append({
                        "Name": row.get("Name"),
                        "Rating": row.get("Rating"),
                        "Cost": row.get("Cost"),
                        "Cuisine": cuisine_str,
                        "Location": row.get("Location"),
                        "Explanation": f"This is one of the highest-rated gems in {row.get('Location')} ({row.get('Rating')}⭐). It matches your preference for {cuisine_str} perfectly!"
                    })
                    seen_names.add(row_name.lower())
        
        # Final safety check: if still under 5, we return what we have
        logger.info(f"Returning {len(final_results)} unique recommendations.")
        return final_results
