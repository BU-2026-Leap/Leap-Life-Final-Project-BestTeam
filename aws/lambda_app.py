from s3_data_fetcher import S3DataFetcher
from common.exam_data_processor import ExamDataProcessor
from common.contracts import read_and_compute
from datetime import datetime

def build_html(stats):
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
        max-width: 600px;
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
      
      .stats-grid {{
        display: grid;
        gap: 20px;
        margin-top: 20px;
      }}
      
      .stat-card {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 24px;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: transform 0.2s ease;
      }}
      
      .stat-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
      }}
      
      .stat-label {{
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.9;
        margin-bottom: 8px;
        font-weight: 500;
      }}
      
      .stat-value {{
        font-size: 2em;
        font-weight: 700;
        font-family: 'Courier New', monospace;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <h1>📊 Stock Tracker</h1>
      <div class="timestamp">⏰ {current_time}</div>
      
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Average Score</div>
          <div class="stat-value">{stats.average_final}</div>
        </div>
        
        <div class="stat-card">
          <div class="stat-label">Unique Students</div>
          <div class="stat-value">{stats.unique_students}</div>
        </div>
      </div>
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