import requests


def get_ton(currency):
    response = "https://api.coinbase.com/v2/exchange-rates?currency=TON"
    json_data = requests.get(response).json()
    try:
        res = json_data['data']['rates'][currency]
    except:
        print('неправильно введена валюта')
        return None
    return res


def convert(count, cost):
    return count / cost
