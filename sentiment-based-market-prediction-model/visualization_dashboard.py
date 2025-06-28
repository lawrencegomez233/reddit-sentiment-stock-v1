import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Reddit Sentiment vs Apple Stock Price")

df = pd.read_csv("sentiment_results/merged_sentiment_stock.csv")
df['Date'] = pd.to_datetime(df['Date'])

st.line_chart(df.set_index('Date')[['Close_AAPL', 'avg_compound']])
st.bar_chart(df.set_index('Date')['num_posts'])