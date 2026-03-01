FROM python:3.13

WORKDIR /app

RUN mkdir -p /app/data

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "4000"]