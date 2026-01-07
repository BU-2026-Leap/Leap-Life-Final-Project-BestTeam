import pathlib
import pytest
import os

def test_csv():

    # Check if 'stocks.csv' exists
    if not pathlib.Path("fetch/stocks.csv").exists():
        raise FileNotFoundError("stocks.csv not found.")
    #
    # else:
    #     df = pd.read_csv("fetch/stocks.csv")
    #
    #     # Check if 'symbol' column exists
    #     if 'symbol' not in df.columns:
    #         raise EmptyHeaderError('Incorrect header.')
    #
    #     # Check if 'symbol' column is empty
    #     if len(df['symbol']) == 0:
    #         raise EmptyDataError("Empty stock list.")
    #
    #     for symbol in df['symbol']:
    #
    #         # Attempt api call
    #         info = finnhub_client.quote(symbol)
    #
    #         # Check if call response is valid
    #         if None in info.values() or 'error' in info.keys():
    #             raise ValueError(f"Invalid stock symbol: {symbol}")

