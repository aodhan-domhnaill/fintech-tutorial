import grpc
import random
import os
import time
import backend_pb2_grpc
import backend_pb2
from google.protobuf.empty_pb2 import Empty
from google.protobuf.timestamp_pb2 import Timestamp


def now():
    t = Timestamp()
    t.GetCurrentTime()
    return t


def backend_stub():
    host = os.getenv("BACKEND_GRPC_HOST")
    return backend_pb2_grpc.PricingStub(
        grpc.insecure_channel(f'{host}:50051')
    )


def integrator(backend_stub):
    price = backend_stub.GetLatestPrice(Empty()).price
    new_price = random.uniform(-100, 100) + price
    print("New Price is random:", new_price, flush=True)
    backend_stub.SavePrice(
        backend_pb2.Stock(
            symbol="RAND",
            price=new_price,
            timestamp=now()
        ),
    )


if __name__ == "__main__":
    stub = backend_stub()

    while True:
        integrator(stub)
        time.sleep(1)
