from aws.s3_data_fetcher import S3DataFetcher
from common.exam_data_processor import ExamDataProcessor
from common.contracts import read_and_compute
from datetime import datetime
from fetch.api import fetch_stocks


def entry(stock, info):
    return f"""
          <tr>
            <td class="ticker">{stock}</td>
            <td class="price">${info["c"]}</td>
            <td class="change {'positive' if info['dp'] > 0 else 'negative'}">{info["dp"]}%</td>
          </tr>
          """
def build_html(stats):

    stocks = fetch_stocks()
    text = '\n'.join([entry(stock, info) for stock, info in stocks.items()])

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Tracker - Dashboard</title>
    <style>
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      
      body {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
      }}
      
      .container {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        padding: 40px;
        max-width: 800px;
        width: 100%;
      }}
      
      h1 {{
        color: #1e3c72;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 10px;
        text-align: center;
        letter-spacing: -0.5px;
      }}
      
      .timestamp {{
        text-align: center;
        color: #666;
        font-size: 0.95em;
        margin-bottom: 30px;
        font-family: 'Courier New', monospace;
        padding: 8px;
        background: #f0f4f8;
        border-radius: 6px;
        display: inline-block;
        width: 100%;
      }}
      
      table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      }}
      
      thead {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
      }}
      
      th {{
        padding: 16px;
        text-align: left;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.85em;
        letter-spacing: 0.5px;
      }}
      
      td {{
        padding: 16px;
        border-bottom: 1px solid #e0e0e0;
        color: #333;
      }}
      
      tbody tr:hover {{
        background: #f5f7fa;
        transition: background 0.2s ease;
      }}
      
      tbody tr:last-child td {{
        border-bottom: none;
      }}
      
      .ticker {{
        font-weight: 600;
        color: #1e3c72;
        font-family: 'Courier New', monospace;
      }}
      
      .price {{
        font-family: 'Courier New', monospace;
        font-weight: 500;
      }}
      
      .change {{
        font-weight: 600;
        font-family: 'Courier New', monospace;
      }}
      
      .positive {{
        color: #22c55e;
      }}
      
      .negative {{
        color: #ef4444;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <h1>📊 Stock Tracker</h1>
      <div class="timestamp">⏰ {current_time}</div>
      
      <table>
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Current Price</th>
            <th>Change</th>
          </tr>
        </thead>
        <tbody>
            {text}
        </tbody>
      </table>
    </div>
  </body>
</html>
"""

def lambda_handler(event, context):
    print("Starting lambda!")

    result = read_and_compute(
        S3DataFetcher("bulead2026-exam-scores", "test_scores.csv"),
        ExamDataProcessor()
    )

    print(result)

    return {
        'statusCode': 200,
        'headers': {"Content-Type": "text/html; charset=utf-8"},
        'body': build_html(result)
    }