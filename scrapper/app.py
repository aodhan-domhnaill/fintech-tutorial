import requests


def handler(event, context):
    requests.get(
        "https://api.coindesk.com/v1/bpi/currentprice.json").json()

    return requests.post("http://api:8000/price/123.0").json()


def avg_handler(event, context):
    try:
        price = requests.get(
            "http://api:8000/mvg_avg/")

    except Exception as e:
        print(f"Error: {e}")
        return {"price": 0}

    price = price.json()
    return price


def storage_handler(event, context):
    price = event['price']

    return requests.post(f"http://api:8000/price/{price}").json()
