FROM python:3.10.4-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/