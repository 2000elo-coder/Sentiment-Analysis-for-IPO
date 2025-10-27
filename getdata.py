import requests
import pandas as pd
import praw
import os
from GoogleNews import GoogleNews

# === Ensure data directory exists ===
os.makedirs('data', exist_ok=True)

# ==============================================================================
#  FUNCTION FROM your ipo_processor.py
# ==============================================================================

def fetch_india_ipos(status="open", api_key="2b95c350ee4bbb2f6bc0d274089f61d07e05ae0864285830dc0987da27dc2e19"):
    """
    Fetch IPOs in India from IPOAlerts API.
    
    Args:
        status (str): one of "open", "upcoming", "closed", "announced", "listed".
        api_key (str): your API key if required.
    Returns:
        pandas.DataFrame: table of IPOs with fields from API.
    """
    base_url = "https://api.ipoalerts.in/ipos"
    params = {"status": status}
    headers = {}
    
    if api_key:
        headers["X-Api-Key"] = api_key
    
    try:
        resp = requests.get(base_url, params=params, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        ipos = data.get("ipos", [])
        df = pd.DataFrame(ipos)
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IPO data: {e}")
        return pd.DataFrame()

# ==============================================================================
#  MAIN SCRIPT LOGIC
# ==============================================================================

if __name__ == "__main__":
    
    # --- 1. Fetch Live Open IPOs ---
    print("Fetching live open IPOs from API...")
    API_KEY = None # Use the default key in the function
    df_open = fetch_india_ipos(status="open", api_key=API_KEY)
    
    if df_open.empty:
        print("No open IPOs found or an error occurred. Exiting.")
    else:
        # Get the list of names. This list will be used for Google News.
        # e.g., ["Company Name Limited", "Another Biz Ltd"]
        open_ipo_names = df_open["name"].to_list()
        
        # For Reddit, a keyword search like "Company Name ipo" is better.
        # e.g., ["Company Name Limited ipo", "Another Biz Ltd ipo"]
        ipo_keywords_reddit = [f"{name} ipo" for name in open_ipo_names]
        
        print(f"Found {len(open_ipo_names)} open IPOs. Proceeding to fetch data...")
        print(open_ipo_names)

        # --- 2. Fetch Reddit Data ---
        print("\n--- Starting Reddit Data Collection ---")
        try:
            reddit = praw.Reddit(
                client_id="KHbmxuI59KvPPjZOuPprvA",
                client_secret="GWtaNscUFjCWPmGJtg0NIaWVCfXSLw",
                user_agent="ipo_sentiment_project"
            )
            subreddits = ['IndianStockMarket', 'IPOIndia', 'StockMarketIndia']
            posts = []

            for sub in subreddits:
                for ipo_keyword, ipo_name in zip(ipo_keywords_reddit, open_ipo_names):
                    print(f"Searching Reddit ({sub}) for: '{ipo_keyword}'")
                    for submission in reddit.subreddit(sub).search(ipo_keyword, limit=50): # Reduced limit to be faster
                        posts.append({
                            'source': 'Reddit',
                            'ipo_name': ipo_name, # Use the proper name
                            'text': submission.title + " " + submission.selftext,
                            'date': submission.created_utc,
                            'upvotes': submission.score,
                            'url': submission.url
                        })

            df_reddit = pd.DataFrame(posts)
            output_path_reddit = 'data/reddit_data.csv'
            df_reddit.to_csv(output_path_reddit, index=False)
            print(f"✅ Reddit data saved to {output_path_reddit} with shape {df_reddit.shape}")
        
        except Exception as e:
            print(f"Error during Reddit data collection: {e}")
            print("Please check your PRAW credentials (client_id, client_secret).")


        # --- 3. Fetch Google News Data ---
        print("\n--- Starting Google News Data Collection ---")
        try:
            googlenews = GoogleNews(lang='en', region='IN', period='30d') # Shorter period for relevance
            all_news = []

            # Use the 'open_ipo_names' list directly
            for ipo in open_ipo_names:
                print(f"Searching Google News for: '{ipo}'")
                googlenews.clear()
                googlenews.search(ipo)
                results = googlenews.result()

                for r in results:
                    all_news.append({
                        'source': 'GoogleNews',
                        'ipo_name': ipo,
                        'title': r.get('title'),
                        'media': r.get('media'),
                        'date': r.get('date'),
                        'desc': r.get('desc'),
                        'link': r.get('link')
                    })

            df_news = pd.DataFrame(all_news)
            output_path_news = 'data/news_data.csv'
            df_news.to_csv(output_path_news, index=False)
            print(f"✅ Collected {len(df_news)} news articles. Saved to {output_path_news}")

        except Exception as e:
            print(f"Error during Google News data collection: {e}")
            print("This may be due to network issues or changes in the GoogleNews library.")
            
        print("\n--- Data Collection Complete ---")
