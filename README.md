podman-compose down && podman-compose build && podman-compose up

to connect to db

* sudo docker ps //to see what's running

copy the name with _db_ on it:  fintech-tutorial_db_1

sudo docker exec -it fintech-tutorial_db_1 /bin/bash

psql -U user db

select * from stock limit 10;

DON'T FORGET THE SEMICOLON DUMBASS!!!!!!!!!!!!!!!!!


to escape:

quit

ctrl + d


to generate the machine generated backend_pb2 py files run: python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. backend.proto

Need to be IN the directory