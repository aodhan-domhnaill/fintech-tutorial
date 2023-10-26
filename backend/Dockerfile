FROM python:3

RUN pip install pytest flake8

WORKDIR /code/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN flake8 *service.py\
    && pytest .
