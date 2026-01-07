import os
import sys

# Ensure the project root is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Temporarily mock boto3 to avoid import errors
sys.modules['boto3'] = type(sys)('boto3')

# Now safely import build_html
from aws.lambda_app import build_html

def main():
    try:
        print("🇯🇲 Fetching live stock data from Finnhub API...")
        
        # Generate HTML with live stock data using lambda_app's build_html
        html_output = build_html(None)
        
        # Save to preview file in project directory
        preview_path = os.path.join(os.path.dirname(__file__), 'live_preview.html')
        with open(preview_path, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print(f"✅ Jamaica-themed preview with minigame generated successfully!")
        print(f"📁 Saved to: {preview_path}")
        
    except Exception as e:
        print(f"❌ Error generating preview: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
