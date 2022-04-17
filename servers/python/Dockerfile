FROM python:3.8


RUN apt-get update && apt-get install -y curl

RUN pip install fastapi uvicorn asyncpg

WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]

