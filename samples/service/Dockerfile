FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY . .

EXPOSE 9000

CMD ["uvicorn", "samples.service.app:app"]