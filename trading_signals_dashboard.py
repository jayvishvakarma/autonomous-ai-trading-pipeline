import streamlit as st
from kafka import KafkaConsumer
import pandas as pd
import json
from datetime import datetime

# --- Streamlit Page Config ---
st.set_page_config(page_title="📈 Trading Signals Dashboard", page_icon="🚀", layout="wide")

# --- Title ---
st.title("📈 Real-Time Trading Signals Dashboard 🚀")
st.caption("Live Buy/Sell Signals based on Sentiment + Price Action 📰💹")

# --- Kafka Consumer Setup ---
consumer = KafkaConsumer(
    'trading-signals',
    bootstrap_servers=['localhost:9092'],  # adjust if needed
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    consumer_timeout_ms=10000
)

# --- Read Kafka Messages ---
records = []

for message in consumer:
    record = message.value
    records.append(record)

# --- Convert to DataFrame ---
if records:
    df = pd.DataFrame(records)

    # Parse time
    if 'signal_time' in df.columns:
        df['signal_time'] = pd.to_datetime(df['signal_time'])

    # Display latest signals first
    df = df.sort_values('signal_time', ascending=False).reset_index(drop=True)

    # --- Color coding for Buy/Sell ---
    def color_signal(val):
        if val == 'BUY':
            return 'background-color: #d4edda; color: green'
        elif val == 'SELL':
            return 'background-color: #f8d7da; color: red'
        else:
            return ''

    # --- Show Last Update Time ---
    st.success(f"✅ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", icon="⏰")

    # --- Show Table ---
    st.subheader("🚀 Live Trading Signals")
    st.dataframe(df.style.applymap(color_signal, subset=['signal']), use_container_width=True)

else:
    st.error("❌ No trading signals received yet from Kafka... 🔄")

