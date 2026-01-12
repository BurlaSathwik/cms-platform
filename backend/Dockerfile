FROM python:3.11

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY alembic.ini .
COPY alembic alembic
COPY app app

# 🔥 THIS LINE WAS MISSING
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
