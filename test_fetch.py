import pathlib
import pytest
import os
from fetch.api import call_api

def test_csv():

    # Check if 'stocks.csv' exists
    if not pathlib.Path("fetch/stocks.csv").exists():
        raise FileNotFoundError("stocks.csv not found.")

    else:
        with pathlib.Path('fetch/stocks.csv').open(mode='r') as file:
            stocks = file.read().split("\n")

        # Check if 'symbol' column exists
        if stocks[0] != 'symbol':
            raise KeyError('Incorrect header.')

        # Check if 'symbol' column is empty
        if len(stocks) < 2:
            raise ValueError("Empty stock list.")

        for symbol in stocks[1:]:

            # Attempt api call
            info = call_api(symbol)

            # Check if call response is valid
            if None in info.values() or 'error' in info.keys():
                raise ValueError(f"Invalid stock symbol: {symbol}")

