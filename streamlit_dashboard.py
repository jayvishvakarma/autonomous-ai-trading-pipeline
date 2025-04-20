import streamlit as st
from kafka import KafkaConsumer
import pandas as pd
import json

st.set_page_config(page_title="News and Price Streaming", page_icon="📈", layout="wide")

# Streamlit Title
st.title("📈 News and Price Streaming Dashboard")

# Kafka Consumer Setup
consumer = KafkaConsumer(
    'news-and-prices',    # <<<--- Corrected topic name!
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    consumer_timeout_ms=10000
)

# Data storage
records = []

# Read messages from Kafka
for message in consumer:
    record = message.value
    records.append(record)

# Create DataFrame
df = pd.DataFrame(records)

if not df.empty:
    # Convert timestamps if they exist
    if 'news_time' in df.columns:
        df['news_time'] = pd.to_datetime(df['news_time'])
    if 'price_time' in df.columns:
        df['price_time'] = pd.to_datetime(df['price_time'])

    # Select required columns
    expected_columns = ['headline', 'sentiment', 'close', 'sma_20', 'sma_50', 'news_time', 'price_time']
    existing_columns = [col for col in expected_columns if col in df.columns]

    final_df = df[existing_columns]

    # Display table
    st.dataframe(final_df, use_container_width=True)

else:
    st.info("No sufficient data available yet from Kafka topic.")
