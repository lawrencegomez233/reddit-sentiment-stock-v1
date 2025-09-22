# reddit-sentiment-stock-v1
A Version 1 project that analyzes Reddit sentiment and compares it to Apple (AAPL) stock price movement. Uses VADER for sentiment scoring, Yahoo Finance for price data, and a Random Forest Classifier to predict price direction.

# Reddit Sentiment vs Apple Stock Price Prediction
# Overview
Made a Python project that checks if Reddit posts about Apple (AAPL) can help predict if the stock will go up or down the next day.

# Steps Taken

1. Scraped Reddit posts from subreddits like r/stocks and r/wallstreetbets.
2. Used VADER (a sentiment tool) to analyze how positive or negative each post was.
3. Added up the average daily sentiment and number of posts.
4. Got Apple's stock prices from Yahoo Finance.
5. Merged the sentiment and price data.
6. Made features such as:
   - Sentiment from yesterday
   - 3-day sentiment average
   - Moving average of stock price
   - Volatility (price changes)
7. Trained a RandomForestClassifier model.
8. The model reached 55.5% accuracy.

# Results
- 55.5% accuracy
- Most helpful features: recent sentiment and stock volatility.
- Visuals show sentiment doesn't always line up with price directly.

# Future Ideas
- Get more Reddit data from more months or years.
- Add news or Twitter sentiment.
- Try different models like XGBoost or LSTM.

# Example Charts
- Line plot: Sentiment vs Apple stock price
