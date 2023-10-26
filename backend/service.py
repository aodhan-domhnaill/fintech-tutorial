import grpc
from concurrent import futures
import time

import backend_pb2_grpc
import backend_pb2
from google.protobuf.timestamp_pb2 import Timestamp

class Pricing(backend_pb2_grpc.PricingServicer):
    def now(self):
        t = Timestamp()
        t.GetCurrentTime()
        return t

    def SavePrice(self, request, context):
        print(request, context)
        return request
    
    def GetLatestPrice(self, request, context):
        return backend_pb2.Stock(
            symbol="AAPL",
            price=123.0,
            timestamp=self.now()
        )

def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    backend_pb2_grpc.add_PricingServicer_to_server(Pricing(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Pricing server started")

if __name__ == "__main__":
    run()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)