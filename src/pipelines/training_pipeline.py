import os
from src.logger import setup_logger
from src.exception import SentimentAnalysisError
from src.components.data_ingestion import DataIngestion
from src.components.data_preprocessing import DataPreprocessing
from src.components.model_trainer import ModelTrainer

logger = setup_logger()

class TrainingPipeline:
    def __init__(self):
        self.raw_data_path = r"C:\Users\mk744\OneDrive - Poornima University\Desktop\Amazon\data\training.1600000.processed.noemoticon (1).csv"
        self.train_path = "artifacts/train.csv"
        self.test_path = "artifacts/test.csv"
        self.tokenizer_path = "artifacts/tokenizer.pkl"
        self.model_path = "artifacts/sentiment_model.keras"
        self.max_features = 10000
        self.max_len = 100
        self.embedding_dim = 128

    def run_pipeline(self):
        try:
            # Data Ingestion
            logger.info("Initiating training pipeline")
            data_ingestion = DataIngestion(self.raw_data_path, self.train_path, self.test_path)
            train_df, test_df = data_ingestion.initiate_data_ingestion()

            # Data Preprocessing
            data_preprocessing = DataPreprocessing(self.max_features, self.max_len)
            X_train, X_test, y_train, y_test, class_weights = data_preprocessing.initiate_data_preprocessing(
                train_df, test_df, self.tokenizer_path
            )

            # Model Training
            model_trainer = ModelTrainer(self.max_features, self.max_len, self.embedding_dim)
            model = model_trainer.build_model()
            history = model_trainer.train_model(X_train, y_train, class_weights, self.model_path)

            logger.info("Training pipeline completed successfully")
            return model, history

        except Exception as e:
            logger.error(f"Error in training pipeline: {str(e)}")
            raise SentimentAnalysisError(f"Training pipeline failed: {str(e)}")