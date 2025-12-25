from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from src.logger import setup_logger
from src.exception import SentimentAnalysisError

logger = setup_logger()

class ModelTrainer:
    def __init__(self, max_features=10000, max_len=100, embedding_dim=128):
        self.max_features = max_features
        self.max_len = max_len
        self.embedding_dim = embedding_dim
        self.model = None

    def build_model(self):
        try:
            logger.info("Building model")
            self.model = Sequential()
            self.model.add(Embedding(self.max_features, self.embedding_dim, input_length=self.max_len))
            self.model.add(Bidirectional(LSTM(64, return_sequences=False)))
            self.model.add(Dropout(0.5))
            self.model.add(Dense(1, activation='sigmoid'))
            
            self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            logger.info("Model compiled successfully")
            return self.model

        except Exception as e:
            logger.error(f"Error building model: {str(e)}")
            raise SentimentAnalysisError(f"Model building failed: {str(e)}")

    def train_model(self, X_train, y_train, class_weights, model_path, epochs=10, batch_size=64):
        try:
            logger.info("Starting model training")
            earlystopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
            
            history = self.model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_split=0.2,
                class_weight=class_weights,
                callbacks=[earlystopping],
                verbose=1
            )
            
            self.model.save(model_path, save_format='keras')
            logger.info(f"Model saved to {model_path}")
            return history

        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise SentimentAnalysisError(f"Model training failed: {str(e)}")