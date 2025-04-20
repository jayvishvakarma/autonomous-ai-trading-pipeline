import streamlit as st
from kafka import KafkaConsumer
import pandas as pd
import json
from datetime import datetime

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Autonomous AI Trading Dashboard 🚀🤖", page_icon="🤖", layout="wide")

# --- Title and Description ---
st.title("🤖 Autonomous AI Trading Dashboard 🚀📈")
st.caption("Real-Time News Sentiment and Price Monitoring 📰📊")

# --- Kafka Consumer Setup ---
consumer = KafkaConsumer(
    'news-and-prices',                  # Correct Kafka topic
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    consumer_timeout_ms=10000            # Stop after 10 seconds if no messages
)

# --- Read data from Kafka topic ---
records = []

for message in consumer:
    record = message.value
    records.append(record)

# --- Create a DataFrame ---
df = pd.DataFrame(records)

if not df.empty:
    # Convert timestamp fields
    if 'news_time' in df.columns:
        df['news_time'] = pd.to_datetime(df['news_time'])
    if 'price_time' in df.columns:
        df['price_time'] = pd.to_datetime(df['price_time'])

    # Keep only relevant columns
    expected_columns = ['headline', 'sentiment', 'close', 'sma_20', 'sma_50', 'news_time', 'price_time']
    existing_columns = [col for col in expected_columns if col in df.columns]
    final_df = df[existing_columns]

    # Sort latest news first
    final_df = final_df.sort_values('news_time', ascending=False).reset_index(drop=True)

    # --- Show Last Update Time ---
    st.success(f"✅ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", icon="⏰")

    # --- Display DataFrame ---
    st.dataframe(final_df, use_container_width=True)

else:
    st.error("❌ Data not found. Waiting for data to arrive from Kafka... 🔄")
