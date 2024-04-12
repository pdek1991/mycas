FROM python
#comment
WORKDIR /root/mycas/SMS-CAS

COPY requirements.txt .

RUN pip install --no-cache-dir -r /root/mycas/SMS-CAS/requirements.txt

VOLUME ["/root/mycas/SMS-CAS"]

COPY . .

EXPOSE 5000
EXPOSE 8080
CMD ["python", "omi.py"]
