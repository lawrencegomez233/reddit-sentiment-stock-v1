# PROCESS: FILE NUMBER THREE

import json
from collections import defaultdict
import pandas as pd
from datetime import datetime

# Load sentiment-analyzed posts
with open("sentiment_results/sentiment_all_matched_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)
    
# Create dictionary to hold lists of sentiments by date
daily_sentiments = defaultdict(list)

# Loop through each post
for post in posts:
    # Convert created_utc to date string
    timestamp = post.get('date')
    if not timestamp:
        continue # skip if no timestamp
    
    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    
    # Get sentiment scores from post
    sentiment = post.get('sentiment', {})
    if sentiment:
        daily_sentiments[date].append(sentiment)
        
# Calculate daily averages as before
daily_averages = []

for date, sentiment_list in daily_sentiments.items():
    count = len(sentiment_list)
    
    avg_pos = sum(s['pos'] for s in sentiment_list) / count
    avg_neg = sum(s['neg'] for s in sentiment_list) / count
    avg_neu = sum(s['neu'] for s in sentiment_list) / count
    avg_compound = sum(s['compound'] for s in sentiment_list) / count
    
    daily_averages.append({
        'date': date,
        'num_posts': count,
        'avg_positive': round(avg_pos, 4),
        'avg_negative': round(avg_neg, 4),
        'avg_neutral': round(avg_neu, 4),
        'avg_compound': round(avg_compound, 4),
    })
    
# Create dataframe and save csv
df = pd.DataFrame(daily_averages)
df = df.sort_values('date')
df.to_csv("sentiment_results/daily_sentiment_summary.csv", index=False)

print("Daily sentiment summary saved to sentiment_results/daily_sentiment_summary.csv")