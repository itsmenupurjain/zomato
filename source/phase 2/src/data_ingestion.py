import pandas as pd
import numpy as np
from datasets import load_dataset
import re
import os
import logging
import sys

# Setup logging for Phase 2
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(log_dir, "data_ingestion.log"))
    ]
)
logger = logging.getLogger("data_ingestion")

def clean_rating(rate_str):
    """Convert rating strings into float values."""
    if pd.isna(rate_str):
        return np.nan
    rate_str = str(rate_str).strip()
    if rate_str in ['NEW', '-', '']:
        return np.nan
    try:
        # Extract the numeric part before /5 if present
        rate_val = rate_str.split('/')[0].strip()
        return float(rate_val)
    except:
        return np.nan

def clean_cost(cost_str):
    """Parse cost strings into numeric integer values representing cost per person."""
    if pd.isna(cost_str):
        return np.nan
    try:
        # Remove commas and extract numbers
        clean_str = str(cost_str).replace(',', '').strip()
        numbers = re.findall(r'\d+', clean_str)
        if numbers:
            # Usually the cost is for two people, so we divide by 2
            return int(numbers[0]) // 2
        return np.nan
    except:
        return np.nan

def clean_cuisines(cuisine_str):
    """Convert comma-separated cuisine strings into clean lists."""
    if pd.isna(cuisine_str):
        return []
    return [c.strip() for c in str(cuisine_str).split(',')]

def standardize_location(loc_str):
    """Standardize location strings to ensure consistent filtering."""
    if pd.isna(loc_str):
        return np.nan
    return str(loc_str).strip().title()

def run_pipeline():
    logger.info("Starting Phase 2: Data Ingestion & Preprocessing")
    
    # 1. Data Acquisition
    logger.info("Downloading dataset 'ManikaSaini/zomato-restaurant-recommendation' from Hugging Face...")
    try:
        dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
        # Load train split into a Pandas DataFrame
        df = dataset['train'].to_pandas()
        logger.info(f"Dataset loaded successfully with shape: {df.shape}")
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        return
        
    # Rename columns to standard names if needed based on typical Zomato datasets
    column_mapping = {
        'approx_cost(for two people)': 'Cost',
        'cost': 'Cost',
        'rate': 'Rating',
        'rating': 'Rating',
        'cuisines': 'Cuisine',
        'cuisine': 'Cuisine',
        'location': 'Location',
        'name': 'Name'
    }
    df.columns = [col.lower() for col in df.columns]
    reverse_mapping = {k.lower(): v for k, v in column_mapping.items()}
    df.rename(columns=reverse_mapping, inplace=True)
    
    logger.info("Applying Data Cleaning & Transformation...")
    
    # 2. Data Cleaning & Transformation
    # Identify critical columns
    critical_columns = ['Name', 'Location', 'Cuisine', 'Rating']
    existing_critical = [col for col in critical_columns if col in df.columns]
    
    # Missing Values: Identify and handle missing or null values in critical columns
    initial_len = len(df)
    df.dropna(subset=existing_critical, inplace=True)
    logger.info(f"Dropped {initial_len - len(df)} rows due to missing critical values.")
    
    # Data Normalization
    if 'Cost' in df.columns:
        df['Cost'] = df['Cost'].apply(clean_cost)
        
    if 'Rating' in df.columns:
        df['Rating'] = df['Rating'].apply(clean_rating)
        
    if 'Cuisine' in df.columns:
        df['Cuisine'] = df['Cuisine'].apply(clean_cuisines)
        
    if 'Location' in df.columns:
        df['Location'] = df['Location'].apply(standardize_location)
        
    # Further clean up any NaNs resulted from parsing in Cost or Rating
    initial_len = len(df)
    check_cols = [col for col in ['Rating', 'Cost'] if col in df.columns]
    if check_cols:
        df.dropna(subset=check_cols, inplace=True)
        logger.info(f"Dropped {initial_len - len(df)} rows due to unparseable rating or cost.")

    # Reset index
    df.reset_index(drop=True, inplace=True)
    
    # 3. Structured Storage
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    output_path = os.path.join(data_dir, "cleaned_restaurants.parquet")
    
    logger.info(f"Exporting cleaned DataFrame to {output_path}...")
    try:
        # Save as parquet, which requires pyarrow or fastparquet installed
        df.to_parquet(output_path, index=False)
        logger.info("Data successfully exported to Parquet format.")
    except Exception as e:
        logger.error(f"Failed to export to Parquet: {e}")
        logger.info("If Parquet export fails due to missing engine, ensure 'pyarrow' or 'fastparquet' is installed.")

if __name__ == "__main__":
    run_pipeline()
