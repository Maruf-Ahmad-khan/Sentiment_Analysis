import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.utils import class_weight
from src.logger import setup_logger
from src.exception import SentimentAnalysisError
from src.utils import save_object

logger = setup_logger()

class DataPreprocessing:
    def __init__(self, max_features=10000, max_len=100):
        self.max_features = max_features
        self.max_len = max_len
        self.tokenizer = None

    def initiate_data_preprocessing(self, train_df, test_df, tokenizer_path):
        try:
            logger.info("Starting data preprocessing")
            
            # Tokenize text
            self.tokenizer = Tokenizer(num_words=self.max_features, oov_token="<OOV>")
            self.tokenizer.fit_on_texts(train_df['text'].astype(str))
            logger.info("Tokenizer fitted on training data")

            # Save tokenizer
            save_object(tokenizer_path, self.tokenizer)

            # Convert text to sequences
            X_train_seq = self.tokenizer.texts_to_sequences(train_df['text'].astype(str))
            X_test_seq = self.tokenizer.texts_to_sequences(test_df['text'].astype(str))
            logger.info("Converted text to sequences")

            # Pad sequences
            X_train = pad_sequences(X_train_seq, maxlen=self.max_len, padding='post', truncating='post')
            X_test = pad_sequences(X_test_seq, maxlen=self.max_len, padding='post', truncating='post')
            logger.info("Padded sequences")

            # Get labels
            y_train = train_df['target'].values
            y_test = test_df['target'].values

            # Calculate class weights
            class_weights = class_weight.compute_class_weight(
                class_weight='balanced',
                classes=np.unique(y_train),
                y=y_train
            )
            class_weights_dict = dict(enumerate(class_weights))
            logger.info("Computed class weights")

            return X_train, X_test, y_train, y_test, class_weights_dict

        except Exception as e:
            logger.error(f"Error in data preprocessing: {str(e)}")
            raise SentimentAnalysisError(f"Data preprocessing failed: {str(e)}")