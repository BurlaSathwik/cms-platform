FROM python:3.11

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
