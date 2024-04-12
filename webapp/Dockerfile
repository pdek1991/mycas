FROM python
#comment
WORKDIR /app/webapp

COPY requirements.txt .

RUN pip install --no-cache-dir -r /app/webapp/requirements.txt

VOLUME ["/app/webapp"]

COPY . .

EXPOSE 8080
CMD ["python", "webpage.py"]
