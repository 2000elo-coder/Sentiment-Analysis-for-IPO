import torch
import joblib
import os
import numpy as np
from transformers import AutoTokenizer, AutoModel

# --- CONFIGURATION ---
MODEL_NAME = 'distilbert-base-uncased'
CLASSIFIER_FILENAME = 'lr_classifier.joblib'

# Check for GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Running on: {device}")

def predict_custom_text():
    # 1. Load the Saved Classifier
    if not os.path.exists(CLASSIFIER_FILENAME):
        print(f"❌ Error: '{CLASSIFIER_FILENAME}' not found.")
        print("Please run your training script first to generate this file.")
        return

    print("Loading models... please wait.")
    classifier = joblib.load(CLASSIFIER_FILENAME)

    # 2. Load BERT (The Feature Extractor)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    bert_model = AutoModel.from_pretrained(MODEL_NAME).to(device)
    bert_model.eval()

    # 3. Take User Input
    print("\n" + "="*50)
    print("ENTER YOUR TEXT BELOW (Press Enter when done):")
    print("="*50)
    user_text = input(">> ")

    if not user_text.strip():
        print("No text entered. Exiting.")
        return

    # 4. Process the Text
    # Tokenize and truncate to 512 tokens (BERT's limit)
    inputs = tokenizer(user_text.lower(), return_tensors="pt", truncation=True, padding=True, max_length=512).to(device)

    # Get Embeddings from BERT
    with torch.no_grad():
        outputs = bert_model(**inputs)
    
    # Extract the 'CLS' token (the vector representing the whole sentence)
    cls_embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()

    # 5. Predict using the Classifier
    prediction_id = classifier.predict(cls_embedding)[0]
    probabilities = classifier.predict_proba(cls_embedding)[0]
    
    # Map ID to Label
    label_map = {0: 'NEGATIVE', 1: 'NEUTRAL', 2: 'POSITIVE'}
    sentiment = label_map[prediction_id]
    confidence = probabilities[prediction_id] * 100

    # 6. Output Result
    print("\n" + "-"*30)
    print(f"SENTIMENT:  {sentiment}")
    print(f"CONFIDENCE: {confidence:.2f}%")
    print("-"*30 + "\n")

if __name__ == "__main__":
    predict_custom_text()