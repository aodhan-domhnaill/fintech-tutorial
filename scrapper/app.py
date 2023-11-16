import requests


def handler(event, context):
    requests.get(
        "https://api.coindesk.com/v1/bpi/currentprice.json").json()

    return requests.post("http://api:8000/price/123.0").json()


def avg_handler(event, context):
    price = requests.get(
        "http://api:8000/mvg_avg/").json()
    return price


def storage_handler(event, context):
    price = event['price']

    return requests.post(f"http://api:8000/price/{price}").json()
