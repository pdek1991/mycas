FROM python
#comment
WORKDIR /root/mycas/STB

COPY requirements.txt .
RUN pip install --no-cache-dir -r /root/mycas/STB/requirements.txt

VOLUME ["/root/mycas/STB"]

COPY . .
CMD ["python", "stb.py"]
