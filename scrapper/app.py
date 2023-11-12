import requests


def handler(event, context):
    requests.get(
        "https://api.coindesk.com/v1/bpi/currentprice.json").json()

    return requests.post("http://api:8000/price/123.0").json()
