import grpc
from concurrent import futures
import time

import backend_pb2_grpc

class Pricing(backend_pb2_grpc.PricingServicer):
    def SavePrice(self, request, context):
        print(request, context)

if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    backend_pb2_grpc.add_PricingServicer_to_server(Pricing(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Pricing server started")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)