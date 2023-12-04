import grpc
from concurrent import futures
import time
import os
import psycopg2

import backend_pb2_grpc
import backend_pb2
from google.protobuf.timestamp_pb2 import Timestamp


class Pricing(backend_pb2_grpc.PricingServicer):
    def __init__(self, conn):
        self.conn = conn

    def _grpc_time(self, dt):
        t = Timestamp()
        t.FromDatetime(dt)
        return t

    def SavePrice(self, request, context):
        with self.conn.cursor() as curs:
            curs.execute(
                "INSERT INTO stock (_time, price, symbol)"
                " VALUES (%s, %s, %s)",
                (request.timestamp.ToDatetime(), request.price, request.symbol)
            )

        self.conn.commit()
        return request

    def GetLatestPrice(self, request, context):
        with self.conn.cursor() as curs:
            curs.execute("SELECT _time, price, symbol FROM stock LIMIT 1")
            obj = curs.fetchone()
            (t, p, s) = obj

        return backend_pb2.Stock(
            symbol=s,
            price=p,
            timestamp=self._grpc_time(t),
        )

    def GetMvgAvg(self, request, context):
        with self.conn.cursor() as curs:
            curs.execute("SELECT price FROM mvg_avg LIMIT 1")
            p = curs.fetchone()

        return backend_pb2.AvgPrice(
            price=p[0],
        )

    def GetSymbols(self, request, context):
        with self.conn.cursor() as curs:
            curs.execute("SELECT * from symbols")
            p = curs.fetchall()
            print(p)

        syms = backend_pb2.Sym()
        for sym in p:
            syms.sym.append(sym[0])

        return syms

def run(dbconn):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    backend_pb2_grpc.add_PricingServicer_to_server(Pricing(dbconn), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Pricing server started")
    return server


if __name__ == "__main__":
    print("Starting backend server")
    uri = os.getenv("POSTGRES_URI")
    print(f"Trying to connect to '{uri}'")
    conn = psycopg2.connect(uri)
    server = run(conn)

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        conn.close()
