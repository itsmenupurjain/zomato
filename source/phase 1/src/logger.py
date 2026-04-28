import logging
import os

def setup_logger(name="zomato_app"):
    """
    Configure and return a basic Python logger to track application events, 
    errors, and LLM API latencies.
    """
    # Create logs directory at the source level
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create handlers if they don't exist
    if not logger.hasHandlers():
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
        
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.INFO)
        
        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)
        
        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        
    return logger

if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Logging setup completed successfully.")
