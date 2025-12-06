# 📊 Financial Sentiment Analysis: LSTM vs. Transformers

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=flat&logo=PyTorch&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=flat&logo=TensorFlow&logoColor=white)
![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97-Hugging%20Face-yellow)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)

## 📖 Project Overview

This project builds and compares two distinct Natural Language Processing (NLP) pipelines to solve a multi-class classification problem: determining whether financial text (news headlines, IPO announcements, corporate statements) is **Negative**, **Neutral**, or **Positive**.

Financial sentiment analysis is notoriously difficult because standard English dictionaries often fail to capture market nuances. For example, words like "volatility" or "correction" have specific financial implications that general sentiment models might miss.

This project pits a **traditional Deep Learning approach (Bi-LSTM)** trained from scratch against a modern **Transfer Learning approach (DistilBERT)** to see which handles this complexity better. The winning model achieves **~90% accuracy** and is deployed via a **Streamlit Web App** for real-time analysis.

---

## 🔬 Methodology & Architecture

We implemented two different architectures to solve the classification task.

### Approach 1: Bidirectional LSTM (The Baseline)
*   **Framework:** TensorFlow / Keras
*   **Architecture:**
    1.  **Tokenization:** Converted text to sequences of integers (Vocabulary size: 10,000).
    2.  **Embedding Layer:** Learned dense vector representations for words from scratch during training.
    3.  **Bidirectional LSTM:** A Recurrent Neural Network (RNN) that processes text sequences both forwards and backwards to capture context.
    4.  **Dense Layers:** Fully connected layers with Softmax activation for 3-class classification.
*   **Outcome:** ~64% Accuracy.
*   **Analysis:** The model suffered from overfitting. While it memorized the training data well, it struggled to generalize to unseen test data, likely because the specific financial dataset was too small to learn complex language representations from scratch.

### Approach 2: DistilBERT + Logistic Regression (The Winner)
*   **Framework:** PyTorch (Hugging Face) + Scikit-Learn
*   **Concept:** **Transfer Learning**. Instead of training embeddings from scratch, we used **DistilBERT**, a smaller, faster, and lighter version of BERT pre-trained on a massive corpus (Wikipedia, BookCorpus).
*   **Architecture:**
    1.  **Feature Extraction:** We passed the financial text through the frozen DistilBERT model. We extracted the **[CLS] token embedding** (a 768-dimensional vector) which encapsulates the semantic meaning of the entire sentence.
    2.  **Classifier:** These rich, context-aware embeddings were fed into a standard **Logistic Regression** classifier.
*   **Outcome:** ~90% Accuracy.
*   **Analysis:** This approach vastly outperformed the LSTM. DistilBERT already "understands" English grammar and context. The classifier only needed to learn the mapping between these high-quality features and the sentiment labels.

---

## 🏆 Results Comparison

The models were evaluated on a held-out test set (20% of data).

| Model Architecture | Test Accuracy | Precision (Macro) | Recall (Macro) | F1-Score (Macro) |
| :--- | :---: | :---: | :---: | :---: |
| **Bi-LSTM** | 64.3% | 0.65 | 0.66 | 0.65 |
| **DistilBERT + LogReg** | **90.4%** | **0.91** | **0.91** | **0.91** |

> **Conclusion:** The Transformer-based approach provides a significant performance boost over training RNNs from scratch for this dataset.

---

## 📂 Repository Structure

```text
├── NLP.ipynb                # Core Notebook: EDA, Preprocessing, Model Training, and Comparison.
├── app.py                   # Streamlit Web Application for GUI inference.
├── cli_inference.py         # Python script for command-line inference.
├── merged_sentiments.csv    # The dataset used for training and testing.
├── lr_classifier.joblib     # The saved Logistic Regression classifier (Artifact).
├── requirements.txt         # List of Python dependencies.
└── README.md                # Project documentation.
For quick testing in your terminal: python cli_inference.py
🔮 Future Improvements
Fine-Tuning: Instead of using DistilBERT as a static feature extractor, we could unfreeze the top layers and fine-tune the Transformer itself for potentially even higher accuracy.
Live Data: Integrate a financial news API (like Yahoo Finance or Alpha Vantage) into the Streamlit app to analyze real-time market news.
Explainability: Implement SHAP or LIME to visualize exactly which words (e.g., "debt," "profit," "IPO") are driving the model's decisions.
