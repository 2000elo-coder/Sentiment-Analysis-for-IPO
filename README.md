Indian IPO Sentiment Analyzer


A data-driven tool to analyze public sentiment for upcoming and current IPOs in the Indian stock market. This project aims to help investors gauge market mood by aggregating and scoring news and social media discussions.

Project Goal

The primary goal of this project is to provide a quantitative sentiment score for current IPOs. By fetching live data on what's currently open (Part 1) and comparing it against the performance of recent, similar IPOs (Part 2), we can apply sentiment analysis (Part 3) to create a data-backed indicator of potential market reception.

This tool is designed to answer: "What is the public's attitude towards an upcoming IPO, and how does that sentiment correlate with the actual performance of recent IPOs?"

Core Features

Live IPO Tracking: Fetches a real-time list of "Open" and "Upcoming" IPOs in the Indian market.

Historical Data Collection: Gathers data on the last 40-50 listed IPOs (spanning 3-5 months) to build a performance benchmark (e.g., issue price, listing price, day 1 gain %).

Sentiment Data Aggregation: Scrapes relevant data for current IPOs from public sources, including:

Reddit: (e.g., r/IndianStockMarket, r/IPOIndia)

Google News: (articles, media mentions)

Sentiment Analysis: Processes the collected text data (titles, posts, article descriptions) to generate a sentiment score (e.g., Positive, Negative, Neutral) for each IPO.

Reporting: Outputs the final analysis to a clean CSV or JSON file for review.