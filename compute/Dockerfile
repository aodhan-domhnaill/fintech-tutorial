FROM python:3.9.18 as builder

RUN pip install pytest flake8

WORKDIR /code/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM python:3.9.18 as compiler

COPY support.cpp support.cpp

RUN g++ -fPIC -shared -o libsupport.so support.cpp

FROM builder as runner

COPY --from=compiler libsupport.so libsupport.so
# RUN clang++ -fPIC -shared -o libsupport.so support.cc
COPY . .

RUN python support.py

RUN flake8 *service.py\
    && pytest .

