import requests
import time
import pandas as pd
from flask import Flask, render_template_string

app = Flask(__name__)

FLINK_REST_API_URL = "http://localhost:9000/v1/sessions"

SQL_QUERY = """
SELECT
    symbol,
    headline,
    sentiment,
    `close`,
    sma_20,
    sma_50,
    news_time,
    price_time
FROM news_and_prices
LIMIT 100
"""

@app.route('/')
def flink_dashboard():
    # Step 1: Create a new session
    session_url = f"{FLINK_REST_API_URL}/v1/sessions"
    response = requests.post(session_url, json={"planner": "blink", "execution-type": "batch"})
    if response.status_code != 200:
        return "Failed to create Flink session!"
    session_id = response.json()['session-id']

    # Step 2: Submit SQL query
    statement_url = f"{FLINK_REST_API_URL}/v1/sessions/{session_id}/statements"
    query_payload = {
        "statement": SQL_QUERY
    }
    response = requests.post(statement_url, json=query_payload)
    if response.status_code != 200:
        return "Failed to submit SQL query!"
    operation_handle = response.json()['operation-handle']

    # Step 3: Poll for query result
    result_url = f"{FLINK_REST_API_URL}/v1/sessions/{session_id}/operations/{operation_handle['handle']}/result"
    timeout_counter = 0
    while timeout_counter < 10:
        result_response = requests.get(result_url)
        if result_response.status_code == 200 and result_response.json()['status'] == "FINISHED":
            break
        time.sleep(2)
        timeout_counter += 1
    else:
        return "Query execution timeout!"

    result_data = result_response.json()

    # Step 4: Parse result
    columns = result_data['columns']
    data = result_data['data']

    df = pd.DataFrame(data, columns=[col['name'] for col in columns])

    # Step 5: Render in HTML
    html = df.to_html(classes='table table-striped', index=False)
    return render_template_string("""
    <html>
    <head>
        <title>📈 News and Price Dashboard</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css">
        <style>
            body { padding: 20px; }
            h1 { margin-bottom: 20px; }
            table { font-size: 14px; }
            .table-container { overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>📈 News and Price Streaming Dashboard</h1>
        <div class="table-container">
            {{table|safe}}
        </div>
    </body>
    </html>
    """, table=html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8502, debug=True)
