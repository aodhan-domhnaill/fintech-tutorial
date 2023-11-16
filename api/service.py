import grpc
import os
import backend_pb2_grpc
import backend_pb2

from google.protobuf.empty_pb2 import Empty
from google.protobuf.timestamp_pb2 import Timestamp

from fastapi import FastAPI

app = FastAPI()


def backend_stub():
    host = os.getenv("BACKEND_GRPC_HOST")
    return backend_pb2_grpc.PricingStub(
        grpc.insecure_channel(f'{host}:50051')
    )


def now():
    t = Timestamp()
    t.GetCurrentTime()
    return t


@app.post("/price/{price}")
def add_price(price: float):
    return _add_price(price, backend_stub=backend_stub())


def _add_price(price, backend_stub):
    backend_stub.SavePrice(
        backend_pb2.Stock(
            symbol="API",
            price=price,
            timestamp=now()
        ),
    )
    return {"price": price}


@app.get("/mvg_avg/")
def get_mvg_avg():
    return _get_mvg_avg(backend_stub=backend_stub())


def _get_mvg_avg(backend_stub):
    price = backend_stub.GetMvgAvg(Empty()).price
    return {"price": price}
