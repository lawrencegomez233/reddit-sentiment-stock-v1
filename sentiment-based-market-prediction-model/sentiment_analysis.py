# PROCESS: FILE NUMBER TWO


# Use VADER (Valence Aware Dictionary for Sentiment Reasoning) for sentiment analysis
# Pre-built sentiment model, great for this project as I am just starting out
# Would be good to look into TextBlob and Hugging Face Transformers
# Pros of VADER:
# 1. Designed for social media language
# 2. No need to train a model myself
# 3. Easy to integrate and fast

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import datetime
import os

# Set up directories
folder = "reddit_data"
filename = "all_matched_posts.json"
filepath = os.path.join(folder, filename)
output_file = "sentiment_all_matched_posts.json"

os.makedirs("sentiment_results", exist_ok=True)

analyzer = SentimentIntensityAnalyzer()

# Load saved posts
with open(filepath, "r", encoding="utf-8") as f:
    posts = json.load(f)

# Analyzise the sentiment of the text in each post
for post in posts:
    text = post["title"] + " " + (post["selftext"] or "")
    sentiment = analyzer.polarity_scores(text)
    compound = sentiment['compound']
    date = datetime.datetime.fromtimestamp(post["date"]).strftime("%Y-%m-%d %H:%M:%S")
    
    # Add sentiment result to each post 
    post["sentiment"] = sentiment
    
    # Save new file with sentiment scores
    with open(os.path.join("sentiment_results", output_file), "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)
    
    # print statements for debugging
    print("Post Title:", post["title"])
    print("Date Posted:", date)
    print("Sentiment Scores:", sentiment)
    
    if compound >= 0.05:
        print("Overall Sentiment: Positive")
    elif compound <= -0.05:
        print("Overall Sentiment: Negative")
    else: 
        print("Overall Sentiment: Neutral")
        
    print("-" * 40)
    
print(f"\nLoaded and analyzed {len(posts)} posts from {filepath}\n")