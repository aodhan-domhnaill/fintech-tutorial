FROM python:3.9.18 as builder

WORKDIR /code/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM builder as tester

RUN pip install pytest flake8

COPY . .

RUN flake8 *service.py\
    && pytest .

FROM builder as runner

COPY . .

ENTRYPOINT [ "python", "/code/service.py" ]
 