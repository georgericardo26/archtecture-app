FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN mkdir -p /code
WORKDIR /code
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
