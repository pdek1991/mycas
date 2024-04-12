FROM python:3.11-alpine3.18

#comment
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r /app/requirements.txt

VOLUME ["/app/CLIENT"]

COPY . .

CMD ["python", "stb_client.py"]

