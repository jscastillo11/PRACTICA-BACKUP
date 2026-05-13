FROM python:3.9-slim-bookworm

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY resources/web /app/web
WORKDIR /app/web

ENV PYTHONUNBUFFERED=1
EXPOSE 5001

CMD ["python", "predict_flask.py"]
