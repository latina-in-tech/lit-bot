FROM python:3.12-rc-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

RUN python seeder.py

CMD ["python", "."]