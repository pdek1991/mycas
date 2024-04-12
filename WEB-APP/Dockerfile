FROM python
#comment
WORKDIR /app/WEB-APP

COPY requirements.txt .

RUN pip install --no-cache-dir -r /app/WEB-APP/requirements.txt

VOLUME ["/app/WEB-APP"]

COPY . .

EXPOSE 8080
CMD ["python", "webpage.py"]
