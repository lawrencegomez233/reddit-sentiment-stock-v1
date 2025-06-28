# PROCESS: FILE NUMBER ONE

# Import Python Reddit API Wrapper (initially testing with this because Twitter requires API keys)
import praw
import datetime
import json
import os
import time
from prawcore.exceptions import RequestException, ResponseException, ServerError, TooManyRequests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access the values
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")
user_agent = os.getenv("USER_AGENT")

# Reddit Credentials
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)

# Define folder for JSON file output or create one if it doesn't exist
output_folder = "reddit_data"
os.makedirs(output_folder, exist_ok=True)

# Choosing subreddits
stock_subreddits = [
    "stocks",
    "investing",
    "wallstreetbets",
    "StockMarket",
    "options",
    "finance",
    "personalfinance",
    "RobinHood",
    "securityanalysis",
    "dividends",
    "ValueInvesting",
    "CryptoCurrency"  # to compare cross-market mood
]

# Define keywords and post count
keywords = [
    "aapl", "$aapl", "apple", "#aapl", "apple stock", "apple inc", "apple earnings"
]
# Additional keywords
keywords += [
    "iphone", "macbook", "tim cook", "apple event", "apple keynote",
    "apple revenue", "apple profit", "apple shares", "apple dividends"
]
limit_per_sub = 100
posts_found = 0

master_matched_posts = [] # Holds ALL matched posts from ALL listed subreddits

# Iterate through subreddits while checking for keywords
for sub in stock_subreddits:
    try:
        subreddit = reddit.subreddit(sub)
        print(f"\nChecking r/{sub}\n")
        
        checked = 0
        matched = 0
        matched_posts = [] # temp list for ONE subreddit
        
        posts = subreddit.search("apple OR AAPL", sort="relevance", time_filter="year", limit=limit_per_sub)
        
        # Pause before pulling from next subreddit to keep traffic polite
        time.sleep(2)
        
        for post in posts: #pull from only relevant posts (may not always be limit)
            post_time = datetime.datetime.fromtimestamp(post.created_utc)
            checked += 1
            text = (post.title + "" + post.selftext).lower()
            
            if any(keyword in text for keyword in keywords):
                matched += 1
                matched_post = ({
                    "title" : post.title,
                    "selftext": post.selftext,
                    "date": post.created_utc,
                    "score": post.score
                })
                matched_posts.append(matched_post) # keep track per sub
                master_matched_posts.append(matched_post) # add to big list
                
                # print output for debugging
                print("Title:", post.title)
                print("Date Posted:", post_time.strftime("%Y-%m-%d %H:%M:%S"))
                print("Text:", post.selftext[:300])  # preview first 300 chars
                print("Subreddit:", sub)
                print("Score:", post.score)
                print("-" * 50)
                posts_found += 1
        # Save individual subreddit data to JSON file for sentiment analysis as a test
        # And build path to save inside folder
        filename = os.path.join(output_folder, f"{sub}_matched_posts.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(matched_posts, f, ensure_ascii=False, indent=4)  
        # Reddit only gives as many posts as it has available and is allowed to return
        # i.e. even if you set 25, Reddit only had 12 to return
        # This is due to Reddit/AutoModerator removing/filtering/deleting posts
        print(f"Found {matched} matching posts out of {checked} posts returned (limit set to {limit_per_sub}) in r/{sub}")
    except TooManyRequests as e:
        print("Rate limited by Reddit. Sleeping for 60 seconds...")
        time.sleep(60)  # back off when told to slow down
    except (RequestException, ResponseException, ServerError) as e:
        print(f"Reddit server or network error: {e}. Retrying in 30 seconds...")
        time.sleep(30)  


# Save all matched posts into one coherent file
filename = os.path.join(output_folder, "all_matched_posts.json")
with open(filename, "w", encoding="utf-8") as f:
    json.dump(master_matched_posts, f, ensure_ascii=False, indent=4)

if posts_found == 0:
    print(f"\n0 total posts found about {keywords}")
else:
    print(f"\nFound {posts_found} total matching posts about {keywords}")
    print(f"Saved {len(master_matched_posts)} total matching posts from all subreddits")