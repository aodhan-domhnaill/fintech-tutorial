import requests


def handler(event, context):
    data = requests.get(
        "https://api.coindesk.com/v1/bpi/currentprice.json").json()

    return data["bpi"]
