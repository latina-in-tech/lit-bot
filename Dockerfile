FROM python:3.12-rc-slim

WORKDIR /app

COPY ./app/ ./app/

RUN pip install -r requirements.txt --no-cache-dir

RUN python seeder.py

CMD ["python", "."]