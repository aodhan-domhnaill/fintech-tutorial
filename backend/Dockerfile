FROM python:3

RUN pip install pytest

WORKDIR /code/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN pwd && ls && pytest .
