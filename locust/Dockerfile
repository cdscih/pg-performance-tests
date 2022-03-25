FROM python:3.8


RUN apt-get update && apt-get install -y curl

RUN pip install asyncpg locust

WORKDIR /app

COPY . .

CMD ["locust"]