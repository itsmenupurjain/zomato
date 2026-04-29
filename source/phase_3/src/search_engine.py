import pandas as pd
import numpy as np
import os
import logging
import sys

# Setup logging for phase_3
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(log_dir, "search_engine.log"))
    ]
)
logger = logging.getLogger("search_engine")

class RestaurantSearchEngine:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self._load_data()

    def _load_data(self):
        logger.info(f"Loading data from {self.data_path}...")
        try:
            self.df = pd.read_parquet(self.data_path)
            logger.info(f"Successfully loaded {len(self.df)} restaurant records.")
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise e

    def _map_budget(self, budget_category: str):
        """Map categorical inputs to numerical cost ranges based on dataset percentiles."""
        if self.df is None or 'Cost' not in self.df.columns:
            return (0, float('inf'))
            
        p33 = self.df['Cost'].quantile(0.33)
        p66 = self.df['Cost'].quantile(0.66)
        
        category = str(budget_category).lower().strip()
        if category == 'low':
            return (0, p33)
        elif category == 'medium':
            return (p33, p66)
        elif category == 'high':
            return (p66, float('inf'))
        else:
            return (0, float('inf')) # Fallback for unknown budgets

    def filter_restaurants(self, location: str = None, max_budget: float = None, cuisines: list = None, min_rating: float = None, top_k: int = 10):
        """Applies boolean masks to the Pandas DataFrame to filter restaurants."""
        if self.df is None:
            logger.error("Data not loaded. Cannot filter.")
            return pd.DataFrame()
            
        mask = pd.Series(True, index=self.df.index)
        
        # 1. Location Filter (Substring match)
        if location:
            mask = mask & self.df['Location'].str.contains(location, case=False, na=False)
            
        # 2. Maximum Budget Filter (User-defined maximum cost)
        if max_budget is not None and max_budget > 0:
            mask = mask & (self.df['Cost'] <= max_budget)
            logger.info(f"Applied maximum budget filter: {max_budget}")
            
        # 3. Cuisine Filter (List intersection)
        if cuisines and len(cuisines) > 0:
            def has_cuisine(cuisine_list):
                if not isinstance(cuisine_list, (list, np.ndarray)):
                    return False
                # Return True if any of the preferred cuisines are in the restaurant's cuisine list
                return any(c.lower().strip() in [rest_c.lower().strip() for rest_c in cuisine_list] for c in cuisines)
            mask = mask & self.df['Cuisine'].apply(has_cuisine)
            
        # 4. Rating Filter (Numerical threshold)
        if min_rating:
            mask = mask & (self.df['Rating'] >= min_rating)
            
        filtered_df = self.df[mask]
        logger.info(f"Filtering applied. {len(filtered_df)} restaurants match the criteria.")
        
        # Sort by rating to return best matches and slice Top K
        if 'Rating' in filtered_df.columns:
            filtered_df = filtered_df.sort_values(by='Rating', ascending=False)
            
        return filtered_df.head(top_k)

    def get_available_locations(self):
        """Returns a sorted list of all unique locations in the database."""
        if self.df is None or 'Location' not in self.df.columns:
            logger.warning("Data not loaded or Location column missing.")
            return []
        
        locations = sorted(self.df['Location'].dropna().unique())
        logger.info(f"Retrieved {len(locations)} unique locations.")
        return locations

    def generate_context(self, filtered_df: pd.DataFrame) -> str:
        """Transforms pre-filtered dataframe rows into a concise string block for the LLM context."""
        if filtered_df.empty:
            return "No matching restaurants found."
            
        context_blocks = []
        for _, row in filtered_df.iterrows():
            name = row.get('Name', 'Unknown')
            # Handle list to string conversion for Cuisines
            cuisine_val = row.get('Cuisine', [])
            cuisine = ", ".join(cuisine_val) if isinstance(cuisine_val, (list, np.ndarray)) else str(cuisine_val)
            
            rating = row.get('Rating', 'N/A')
            cost = row.get('Cost', 'N/A')
            location = row.get('Location', 'Unknown')
            
            context = f"Name: {name}, Cuisine: {cuisine}, Rating: {rating}, Cost: {cost}, Location: {location}"
            context_blocks.append(context)
            
        full_context = "\n".join(context_blocks)
        logger.info(f"Generated context string for {len(filtered_df)} restaurants.")
        return full_context

if __name__ == "__main__":
    # Example testing code
    current_dir = os.path.dirname(os.path.dirname(__file__))
    
    # We point to the cleaned data generated in phase_2
    # Assuming phase_2 and phase_3 are side-by-side in the 'source' folder
    phase2_data_file = os.path.join(os.path.dirname(current_dir), "phase_2", "data", "cleaned_restaurants.parquet")
    
    if os.path.exists(phase2_data_file):
        engine = RestaurantSearchEngine(phase2_data_file)
        
        # Simulated User Preferences
        test_location = "Indiranagar"
        test_budget = "Medium"
        test_cuisines = ["Italian", "Cafe"]
        test_min_rating = 4.0
        
        logger.info(f"Test Query -> Location: {test_location}, Budget: {test_budget}, Cuisines: {test_cuisines}, Min Rating: {test_min_rating}")
        
        results = engine.filter_restaurants(
            location=test_location,
            budget=test_budget,
            cuisines=test_cuisines,
            min_rating=test_min_rating,
            top_k=5
        )
        
        context_string = engine.generate_context(results)
        print("\n--- LLM Context Block ---")
        print(context_string)
        print("-------------------------")
    else:
        logger.warning(f"Data file not found at {phase2_data_file}. Please run phase_2 data ingestion first.")
