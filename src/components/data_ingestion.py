import pandas as pd
import os
from sklearn.model_selection import train_test_split
from src.logger import setup_logger
from src.exception import SentimentAnalysisError

logger = setup_logger()

class DataIngestion:
    def __init__(self, raw_data_path, train_path, test_path):
        self.raw_data_path = raw_data_path
        self.train_path = train_path
        self.test_path = test_path

    def initiate_data_ingestion(self):
        try:
            logger.info("Starting data ingestion")
            df = pd.read_csv(
                self.raw_data_path,
                encoding='ISO-8859-1',
                header=None,
                names=["target", "ids", "date", "flag", "user", "text"],
                on_bad_lines='skip',
                engine='python'
            )
            logger.info(f"Loaded dataset with {len(df)} rows")

            # Clean labels: 0 = negative, 4 = positive → binary
            df['target'] = df['target'].replace({0: 0, 4: 1})
            df = df[df['target'].isin([0, 1])]

            # Sample smaller size for fast training
            df = df.sample(n=100000, random_state=42).reset_index(drop=True)
            logger.info(f"Sampled dataset to {len(df)} rows")

            # Split features and labels
            X = df['text'].astype(str)
            y = df['target'].values

            # Train/test split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, stratify=y, random_state=42
            )
            logger.info(f"Train set: {len(X_train)} samples, Test set: {len(X_test)} samples")

            # Save train and test sets
            train_df = pd.DataFrame({'text': X_train, 'target': y_train})
            test_df = pd.DataFrame({'text': X_test, 'target': y_test})
            train_df.to_csv(self.train_path, index=False)
            test_df.to_csv(self.test_path, index=False)
            logger.info(f"Saved train data to {self.train_path} and test data to {self.test_path}")

            return train_df, test_df

        except Exception as e:
            logger.error(f"Error in data ingestion: {str(e)}")
            raise SentimentAnalysisError(f"Data ingestion failed: {str(e)}")