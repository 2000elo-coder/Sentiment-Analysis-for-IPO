import streamlit as st
import joblib
import torch
import numpy as np
import os
from transformers import AutoTokenizer, AutoModel

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Financial Sentiment Analyzer",
    page_icon="📊",
    layout="centered"
)

# --- CONSTANTS ---
MODEL_NAME = 'distilbert-base-uncased'
CLASSIFIER_FILENAME = 'lr_classifier.joblib'
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- LOAD MODELS (CACHED) ---
# We use @st.cache_resource so the model loads once and stays in memory
@st.cache_resource
def load_pipeline():
    """
    Loads the Tokenizer, BERT Model, and Logistic Regression Classifier.
    Returns None if the classifier file is missing.
    """
    try:
        # 1. Load Classifier
        if not os.path.exists(CLASSIFIER_FILENAME):
            return None, None, None

        classifier = joblib.load(CLASSIFIER_FILENAME)

        # 2. Load BERT
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        bert_model = AutoModel.from_pretrained(MODEL_NAME).to(DEVICE)
        bert_model.eval()

        return tokenizer, bert_model, classifier
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None

# --- INFERENCE FUNCTION ---
def predict_sentiment(text, tokenizer, bert_model, classifier):
    # Tokenize (Truncate to 512 tokens)
    inputs = tokenizer(text.lower(), return_tensors="pt", truncation=True, padding=True, max_length=512).to(DEVICE)

    # Generate Embeddings
    with torch.no_grad():
        outputs = bert_model(**inputs)
    
    # Extract CLS token
    cls_embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()

    # Predict
    prediction_id = classifier.predict(cls_embedding)[0]
    probabilities = classifier.predict_proba(cls_embedding)[0]

    # Map to labels
    label_map = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
    sentiment = label_map[prediction_id]
    confidence = probabilities[prediction_id]

    return sentiment, confidence

# --- MAIN UI ---
def main():
    st.title("📊 Financial Sentiment AI")
    st.write("Paste a financial news snippet, IPO details, or a market statement below to analyze its sentiment.")

    # Load models with a spinner
    with st.spinner("Loading AI Models..."):
        tokenizer, bert_model, classifier = load_pipeline()

    if classifier is None:
        st.error(f"Could not find '{CLASSIFIER_FILENAME}'. Please make sure the training file is in the same directory.")
        st.stop()

    # Input Area
    user_text = st.text_area("Enter Text:", height=200, placeholder="E.g., The company reported record profits this quarter...")

    # Analyze Button
    if st.button("Analyze Sentiment", type="primary"):
        if not user_text.strip():
            st.warning("Please enter some text first.")
        else:
            # Run Prediction
            sentiment, confidence = predict_sentiment(user_text, tokenizer, bert_model, classifier)
            
            # Display Results
            st.divider()
            
            # Dynamic Color Formatting
            if sentiment == "Positive":
                st.success(f"### Sentiment: {sentiment.upper()} ")
            elif sentiment == "Negative":
                st.error(f"### Sentiment: {sentiment.upper()} ")
            else:
                st.info(f"### Sentiment: {sentiment.upper()} ")
            
            # Display Confidence Meter
            st.write(f"**Confidence Score:** {confidence:.2%}")
            st.progress(float(confidence))

    # Footer
    st.markdown("---")
    st.caption(f"Running on: {DEVICE} | Model: DistilBERT + Logistic Regression")

if __name__ == "__main__":
    main()