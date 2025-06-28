# PROCESS: FILE NUMBER FOUR


# Obtain stock data for Apple from Yahoo Finance
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load sentiment CSV produced file from aggregate_sentiment.py
sentiment_df = pd.read_csv("sentiment_results/daily_sentiment_summary.csv")

# Get stock prices for Apple for the same date range as sentiment
start_date = sentiment_df['date'].min()
end_date = sentiment_df['date'].max()

# Download daily data from yfinance
stock_data = yf.download("AAPL", start=start_date, end=end_date)
print("Stock data downloaded")

# Prepare stock price data and reset index to have 'date' as a column
stock_data.reset_index(inplace=True)

# Flatten MultiIndex columns in stock_data
stock_data.columns = ['_'.join(filter(None, col)).strip() for col in stock_data.columns.values]

sentiment_df['date'] = pd.to_datetime(sentiment_df['date'], errors='coerce')
stock_data['Date'] = pd.to_datetime(stock_data['Date'], errors='coerce')

# Merge sentiment and stock price on the date
merged_df = pd.merge(sentiment_df, stock_data, left_on='date', right_on='Date')

# Save merged data frame to file for later use
merged_df.to_csv("sentiment_results/merged_sentiment_stock.csv", index=False)

# Begin plot
fig, ax1 = plt.subplots(figsize=(14, 6))

# Plot AAPL Close Price
ax1.plot(merged_df['Date'], merged_df['Close_AAPL'], color='blue', label='AAPL Close Price')
ax1.set_xlabel("Date")
ax1.set_ylabel('AAPL Close Price', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Add sentiment to secondary y-axis
ax2 = ax1.twinx()
ax2.plot(merged_df['Date'], merged_df['avg_compound'], color='orange', label='Sentiment Compound')
ax2.set_ylabel('Sentiment Compound', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

# Format x-axis
ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
fig.autofmt_xdate()

plt.title("Apple Stock Price and Sentiment Over Time")
fig.tight_layout()
plt.show()
print("Plotting done.")

# Calculate simple correlation between sentiment and price
correlation = merged_df['avg_compound'].corr(merged_df['Close_AAPL'])
print(f"Correlation between sentiment compound score and closing price: {correlation:.4f}")