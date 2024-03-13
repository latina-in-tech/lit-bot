FROM python:3.12-rc-slim

WORKDIR /app

COPY /app .

RUN apt-get update && \
    apt-get install sqlite3

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "."]