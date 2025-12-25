import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from src.logger import setup_logger
from src.exception import SentimentAnalysisError
from src.utils import load_object

logger = setup_logger()

class PredictionPipeline:
    def __init__(self, model_path, tokenizer_path, max_len=100):
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.max_len = max_len
        self.model = None
        self.tokenizer = None

    def load_resources(self):
        try:
            logger.info("Loading model and tokenizer")
            self.model = load_model(self.model_path)
            self.tokenizer = load_object(self.tokenizer_path)
            logger.info("Resources loaded successfully")
        except Exception as e:
            logger.error(f"Error loading resources: {str(e)}")
            raise SentimentAnalysisError(f"Resource loading failed: {str(e)}")

    def predict(self, text):
        try:
            if not self.model or not self.tokenizer:
                self.load_resources()
            
            # Preprocess input text
            seq = self.tokenizer.texts_to_sequences([text])
            padded = pad_sequences(seq, maxlen=self.max_len, padding='post', truncating='post')
            
            # Predict
            prediction = self.model.predict(padded, verbose=0)[0][0]
            sentiment = "Positive" if prediction >= 0.5 else "Negative"
            confidence = prediction if prediction >= 0.5 else 1 - prediction
            
            logger.info(f"Prediction for '{text[:50]}...': {sentiment} ({confidence:.2f})")
            return sentiment, confidence

        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            raise SentimentAnalysisError(f"Prediction failed: {str(e)}")