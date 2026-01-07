from s3_data_fetcher import S3DataFetcher
from exam_data_processor import ExamDataProcessor
from contracts import read_and_compute

def build_html(stats):
    return f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Summary of All</title>
  </head>
  <body>
    <h1>Student Scores!</h1>
    <ul>
      <li><strong>Average score:</strong> {stats.average_final}</li>
      <li><strong>Unique students:</strong> {stats.unique_students}</li>
    </ul>
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