FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 SOURCE_DATE_EPOCH=0
WORKDIR /app
COPY requirements.lock .
RUN pip install --no-cache-dir --require-hashes -r requirements.lock
COPY . .
RUN python scripts/verify_integrity.py && python scripts/verify_axiom_consistency.py
EXPOSE 8080
CMD ["python", "api_server.py"]