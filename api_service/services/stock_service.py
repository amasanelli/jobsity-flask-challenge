import requests

class StockService():

    url = 'http://127.0.0.1:5001/api/v1/stock?stockCode={}'

    @classmethod
    def get_data(cls, stock_code: str):
        res = requests.get(cls.url.format(stock_code))

        if res.status_code != 200:
            raise Exception(res.text)

        return res.json()