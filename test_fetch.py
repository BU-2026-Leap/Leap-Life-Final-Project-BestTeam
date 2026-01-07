import pathlib
import pandas as pd
import pytest
from pandas.errors import EmptyDataError
from tarfile import EmptyHeaderError
import finnhub
import os

finnhub_client = finnhub.Client(api_key=os.environ['API_KEY'])

def test_csv():

    # Check if 'stocks.csv' exists
    if not pathlib.Path("stocks.csv").exists():
        raise FileNotFoundError("stocks.csv not found.")

    else:
        df = pd.read_csv("stocks.csv")

        # Check if 'symbol' column exists
        if 'symbol' not in df.columns:
            raise EmptyHeaderError('Incorrect header.')

        # Check if 'symbol' column is empty
        if len(df['symbol']) == 0:
            raise EmptyDataError("Empty stock list.")

        for symbol in df['symbol']:

            # Attempt api call
            info = finnhub_client.quote(symbol)

            # Check if call response is valid
            if None in info.values() or 'error' in info.keys():
                raise ValueError(f"Invalid stock symbol: {symbol}")

