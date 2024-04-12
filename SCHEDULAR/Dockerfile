FROM python
#comment
WORKDIR /root/mycas/SCHEDULAR

COPY requirements.txt .
RUN pip install --no-cache-dir -r /root/mycas/SCHEDULAR/requirements.txt

VOLUME ["/root/mycas/SCHEDULAR"]

COPY . .
CMD ["python", "schedular.py"]
