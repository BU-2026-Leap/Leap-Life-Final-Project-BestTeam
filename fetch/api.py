import os
import finnhub
import pandas as pd

finnhub_client = finnhub.Client(api_key=os.environ['API_KEY'])

def fetch_stocks() -> pd.DataFrame:

    df = pd.read_csv("fetch/stocks.csv")

    return pd.DataFrame([finnhub_client.quote(symbol) for symbol in df['symbol']], index=df['symbol'])

if __name__ == "__main__":
    output = fetch_stocks()





