import os
import urllib3
import pathlib

def call_api(symbol:str):
    response = urllib3.request(method='GET', url='https://finnhub.io/api/v1/quote',
                               headers={'X-Finnhub-Token': os.environ['API_KEY']},
                               fields={'symbol': symbol})

    return eval(response.data.decode('UTF-8-sig'))

def fetch_stocks() -> dict:

    with pathlib.Path('fetch/stocks.csv').open(mode='r') as file:
        stocks = file.read().split("\n")[1:]

    return {stock: call_api(stock) for stock in stocks}

if __name__ == "__main__":
    output = fetch_stocks()



