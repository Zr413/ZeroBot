import requests
import json
from config import keys


class ConvetrionExeption(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvetrionExeption(f'Введены одинаковые валюты {base}.')

        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise ConvetrionExeption(f'Не удалось обработать валюту {quote}')

        try:
            base_ticket = keys[base]
        except KeyError:
            raise ConvetrionExeption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvetrionExeption(f'Не удалось обработать количество {amount}')

        conv = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticket}&tsyms={base_ticket}')
        total_base = json.loads(conv.content)[keys[base]]

        return  total_base