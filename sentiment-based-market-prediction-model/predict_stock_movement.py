# PROCESS: FILE NUMBER FIVE

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
# ML for simple predictive model

# Load merged sentiment and stock price data
merged_df = pd.read_csv("sentiment_results/merged_sentiment_stock.csv") 

# Make sure date is datetime and sort
merged_df['Date'] = pd.to_datetime(merged_df['Date'])
merged_df = merged_df.sort_values('Date').reset_index(drop=True)

# Create lagged sentiment features
merged_df['avg_compound_lag1'] = merged_df['avg_compound'].shift(1)
merged_df['avg_compound_lag2'] = merged_df['avg_compound'].shift(2)

# Sentiment rolling average (3-day)
merged_df['sentiment_roll_3'] = merged_df['avg_compound'].rolling(window=3).mean()

# Technical indicators from stock prices
merged_df['MA_5'] = merged_df['Close_AAPL'].rolling(window=5).mean()
merged_df['Return_1'] = merged_df['Close_AAPL'].pct_change()
merged_df['Volatility_5'] = merged_df['Return_1'].rolling(window=5).std()

# Use post count per day
merged_df['num_posts'] = merged_df['num_posts'].fillna(0)

# Engineer other interaction features
merged_df['sentiment_x_return'] = merged_df['avg_compound'] * merged_df['Return_1']
merged_df['return_x_volatility'] = merged_df['Return_1'] * merged_df['Volatility_5']
merged_df['sentiment_x_posts'] = merged_df['avg_compound'] * merged_df['num_posts']

# Create target variables, 1 if next day close is greater than today's close, else 0
merged_df['next_close'] = merged_df['Close_AAPL'].shift(-1)
merged_df['price_up'] = (merged_df['next_close'] > merged_df['Close_AAPL']).astype(int)

# Drop rows with missing values due to shifting
merged_df = merged_df.dropna(subset=['avg_compound_lag1', 'avg_compound_lag2', 'sentiment_x_return',
                                     'sentiment_roll_3', 'MA_5', 'Return_1', 'Volatility_5', 
                                     'sentiment_x_posts', 'return_x_volatility', 'price_up'])

# Define features and target
features = [
    'avg_compound', 'avg_compound_lag1', 'avg_compound_lag2', 'sentiment_roll_3',
    'num_posts', 'MA_5', 'Return_1', 'Volatility_5',
    'sentiment_x_return', 'sentiment_x_posts', 'return_x_volatility'
]
X = merged_df[features]
y = merged_df['price_up']

# Split data into train and test sets while keeping time order
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Scale features
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=features)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=features)

# Train logistic regression with class weights
#model = LogisticRegression(class_weight='balanced', max_iter=1000)
#model.fit(X_train, y_train)

# Train Random Forest with class weights to balance classes
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=6,
    min_samples_split=4,
    class_weight='balanced',
    random_state=42
)

model.fit(X_train_scaled, y_train)

# Predict using test data
y_pred = model.predict(X_test)

# Print data size
print(f"Total rows in dataset: {len(merged_df)}")

# Print accuracy and classification reports
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Print model coefficient
#print(f"Model coefficient for avg_compound: {model.coef_[0][0]:.4f}")

# Feature importances
for feature, importance in zip(features, model.feature_importances_):
    print(f"Feature importance for {feature}: {importance:.4f}")
    
# Plot actual vs predicted
plt.figure(figsize=(12, 5))
plt.plot(y_test.values, label='Actual')
plt.plot(y_pred, label='Predicted', linestyle='--')
plt.title("Actual vs Predicted Price Movement")
plt.legend()
plt.show()