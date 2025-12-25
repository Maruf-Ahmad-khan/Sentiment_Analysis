import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from src.pipelines.prediction_pipeline import PredictionPipeline
from src.logger import setup_logger

# Initialize logger
logger = setup_logger()

# Initialize prediction pipeline
@st.cache_resource
def load_prediction_pipeline():
    try:
        pipeline = PredictionPipeline(
            model_path=r"C:\Users\mk744\OneDrive - Poornima University\Desktop\Amazon\artifacts\sentiment_model.keras",
            tokenizer_path=r"C:\Users\mk744\OneDrive - Poornima University\Desktop\Amazon\artifacts\tokenizer.pkl",
            max_len=100
        )
        pipeline.load_resources()
        logger.info("Prediction pipeline loaded successfully")
        return pipeline
    except Exception as e:
        logger.error(f"Error loading prediction pipeline: {str(e)}")
        st.error(f"Failed to load model or tokenizer: {str(e)}")
        return None


# App UI
st.set_page_config(page_title="Sentiment Predictor", layout="wide", initial_sidebar_state="expanded")


# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This app predicts the sentiment (positive or negative) of a text review using a trained RNN model.
    Enter your review in the main panel and click 'Predict Sentiment' to see the result.
    """)
    st.markdown("---")
    st.subheader("🛠️ Settings")
    st.info("Model and tokenizer are loaded from artifacts. Ensure they exist in the artifacts folder.")


# Main content
st.title("🧠 Sentiment Prediction App")
st.markdown("Enter a review below to get an instant sentiment prediction (Positive or Negative).")


# Responsive container for input
with st.container():
    review = st.text_area("✍️ Enter your review:", height=150, placeholder="Type your review here...")


# Prediction button
if st.button("Predict Sentiment", use_container_width=True):
    if review.strip() == "":
        st.warning("Please enter some text to analyze.")
    else:
        # Load pipeline
        pipeline = load_prediction_pipeline()
        if pipeline is None:
            st.stop()

        # Make prediction
        try:
            sentiment, confidence = pipeline.predict(review)
            score = confidence if sentiment == "Positive" else 1 - confidence

            # Responsive layout with columns
            col1, col2 = st.columns([1, 1], gap="medium")

            # Prediction result
            with col1:
                st.subheader("🧾 Prediction Result")
                st.metric(label="Sentiment", value=sentiment, delta=f"Score: {score:.4f}")
                st.write(f"**Confidence**: {confidence*100:.0f}%")  # Formatted as percentage (e.g., 12%)

            # Pie chart
            with col2:
                st.subheader("📊 Confidence Chart")
                labels = ['Positive', 'Negative']
                values = [confidence if sentiment == "Positive" else 1 - confidence,
                          1 - confidence if sentiment == "Positive" else confidence]
                colors = ['#4CAF50', '#F44336']  # Green for Positive, Red for Negative

                fig, ax = plt.subplots(figsize=(5, 2))
                ax.pie(values, labels=labels, colors=colors, autopct='%1.0f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
                ax.set_title("Model Confidence")
                
                # Ensure tight layout for responsiveness
                plt.tight_layout()
                st.pyplot(fig)

        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            st.error(f"Error during prediction: {str(e)}")


# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Model trained on Sentiment140 dataset")