# 🇮🇳 **Indian IPO Sentiment Analyzer**

### 📊 *A Data-Driven Tool for Analyzing Public Sentiment on Indian IPOs*

---

## 🧭 **Overview**

The **Indian IPO Sentiment Analyzer** is a data-driven project that helps investors gauge the **market mood** toward **upcoming and current IPOs** in the Indian stock market.  

It aggregates and analyzes **news articles**, **Reddit discussions**, and other public data sources to generate a **sentiment score** — indicating whether public opinion around an IPO is **Positive**, **Negative**, or **Neutral**.

---

## 🎯 **Project Goal**

The main objective of this project is to provide a **quantitative sentiment indicator** for ongoing IPOs.

It achieves this through a **three-part pipeline**:

1. **Live Data Fetching:** Identify and list all *open* and *upcoming* IPOs from reliable financial sources.  
2. **Historical Benchmarking:** Compare sentiment and performance metrics with **recent IPOs** (e.g., issue price, listing gain, etc.).  
3. **Sentiment Scoring:** Analyze aggregated public discussions to produce a **sentiment score** per IPO.

> 💡 *Answering the question:*  
> “What is the public’s attitude toward an upcoming IPO, and how does that sentiment correlate with its actual market performance?”

---

## ⚙️ **Core Features**

### 🔹 **1. Live IPO Tracking**
- Fetches a **real-time list** of currently *Open* and *Upcoming* IPOs in the Indian market.  
- Uses web scraping or API-based data collection from financial websites (e.g., *MoneyControl*, *Chittorgarh*).

---

### 🔹 **2. Historical Data Collection**
- Collects data on **recently listed IPOs** (around the last *40–50* entries, covering 3–5 months).  
- Builds a performance benchmark with details such as:
  - Issue Price  
  - Listing Price  
  - Day-1 Gain (%)  

---

### 🔹 **3. Sentiment Data Aggregation**
- Gathers relevant text data from:
  - 🗞 **Google News** (media articles, coverage frequency)
  - 💬 **Reddit** (e.g., `r/IndianStockMarket`, `r/IPOIndia`)
- Extracts post titles, article descriptions, and comments related to each IPO.

---

### 🔹 **4. Sentiment Analysis**
- Uses **Natural Language Processing (NLP)** techniques to evaluate overall sentiment.
- Assigns each IPO one of the following sentiment categories:
  - 🟢 **Positive**
  - 🟠 **Neutral**
  - 🔴 **Negative**