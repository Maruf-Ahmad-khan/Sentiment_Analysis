import pickle
import os
from src.logger import setup_logger
from src.exception import SentimentAnalysisError

logger = setup_logger()

def save_object(file_path, obj):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            pickle.dump(obj, f)
        logger.info(f"Object saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving object to {file_path}: {str(e)}")
        raise SentimentAnalysisError(f"Failed to save object: {str(e)}")

def load_object(file_path):
    try:
        with open(file_path, "rb") as f:
            obj = pickle.load(f)
        logger.info(f"Object loaded from {file_path}")
        return obj
    except Exception as e:
        logger.error(f"Error loading object from {file_path}: {str(e)}")
        raise SentimentAnalysisError(f"Failed to load object: {str(e)}")