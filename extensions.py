import requests
import json


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{base}"
            response = requests.get(url)
            data = response.json()

            if quote not in data["rates"]:
                raise APIException("Неверное имя валюты.")

            rate = data["rates"][quote]
            result = amount * rate
            return result
        except Exception as e:
            raise APIException("Не удалось получить курс валюты.")
class APIException(Exception):
    def _init_(self, text):
        self.text = text