import requests
import csv
from datetime import datetime


class Stooq():
    url = 'https://stooq.com/q/l/?s={}&f=sd2t2ohlcvn&h&e=csv'

    @classmethod
    def get_data(cls, stock_code: str):
        res = requests.get(cls.url.format(stock_code))

        decoded = res.content.decode('utf-8')

        lst = list(csv.reader(decoded.splitlines(), delimiter=','))

        if 'N/D' in lst[1]:
            raise Exception('No data')

        return cls._format_data(lst)

    @staticmethod
    def _format_data(lst):

        keys = [item.lower() for item in lst[0]]
        values = lst[1]

        obj = dict(zip(keys, values))

        obj['date'] = datetime.strptime(obj['date'], '%Y-%m-%d')
        obj['time'] = datetime.strptime(obj['time'], '%H:%M:%S').time()

        return obj
