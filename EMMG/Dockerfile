FROM python:3.8.19
#comment
WORKDIR /app/emmg

COPY requirements.txt .
RUN pip install --no-cache-dir -r /app/emmg/requirements.txt

VOLUME ["/app/emmg"]

COPY . .
CMD ["python", "emmg.py"]
