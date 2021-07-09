FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
ADD . /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get upgrade -y
RUN apt-get install sqlite3 libsqlite3-dev -y
COPY . /app