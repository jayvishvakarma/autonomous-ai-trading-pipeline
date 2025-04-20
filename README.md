# Autonomous AI Trading Pipeline 🚀📈
Real-Time Financial News Sentiment Analysis and Stock Price Correlation with Autonomous Trading Signal Generation.
---

## 📚 Project Overview

This project builds a real-time **Autonomous AI Trading Pipeline** that:

- Ingests live **financial news** and **stock prices**.
- Performs **sentiment analysis** using **Azure OpenAI GPT models**.
- Processes data streams in **real-time** using **Apache Flink SQL**.
- Generates actionable **BUY/SELL trading signals**.
- Visualizes sentiment trends, price movements, and trading decisions via a **Streamlit dashboard**.
- Entire system is deployed using **Docker-Compose** for modular orchestration.

Initially focused on US markets, the architecture is **future-ready for Indian stock markets (NSE/BSE)** and **real-time Twitter/News ingestion with Agentic AI-based decision-making**.
---

## 🏗️ Architecture Diagram

![image](https://github.com/user-attachments/assets/77ca7439-702d-4c41-90aa-06d63c8a7aac)

## 🚀 Technology Stack

Component | Technology
Data Streaming | Redpanda (Kafka-compatible)
Stream Processing | Apache Flink SQL
Sentiment Analysis | Azure OpenAI (GPT-3.5)
Visualization | Streamlit
Deployment | Docker-Compose
Programming Language | Python 3.8+
Financial Data Source | Alpaca Market Data API

## 🛠️ Setup Instructions
### 1. Clone the Repository

git clone https://github.com/jayvishvakarma/autonomous-ai-trading-pipeline.git
cd autonomous-ai-trading-pipeline

### 2. Configure API Keys
alpaca_config/keys.py
utils.py

### 3. Start the Infrastructure
docker-compose up -d

This will start:
Redpanda Brokers
Redpanda Console (Web UI)
Flink SQL JobManager and TaskManager
SQL Gateway for submitting Flink queries
✅ Access Redpanda Console at: http://localhost:8080
✅ Access Flink Dashboard at: http://localhost:8081

### 4. Run the Producers

python news-producer.py
python prices-producer.py

### 5. Submit Flink SQL Jobs
Connect to Flink SQL Gateway using provided script:
docker exec -it sql-client bash
Run the DDL statements inside ddl.sql to create tables and views.

### 6. Start the Streamlit Dashboard
streamlit run streamlit_dashboard.py

✅ Access the dashboard at: http://localhost:8501

## 📈 Features
Real-time ingestion of financial news and stock price streams.
Sentiment analysis using LLMs (Azure OpenAI GPT models).
Real-time moving average (SMA-20, SMA-50) calculations.
Trading Signal Generation (BUY/SELL based on sentiment and SMA crossovers).
Interactive monitoring dashboard showing live trading conditions.

# 👨‍💻 Executed By
### Preeti Vishvakarma -> Roll Number: M24DE2021; Email: M24DE2021@iitj.ac.in

### Jay Vishvakarma -> Roll Number: M24DE2011; Email: M24DE2011@iitj.ac.in

# 📄 License
This project is developed for academic and research purposes under supervision at IIT Jodhpur.
