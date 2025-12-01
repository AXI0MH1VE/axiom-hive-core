FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 SOURCE_DATE_EPOCH=0
WORKDIR /app
COPY requirements.lock .
RUN pip install --no-cache-dir -r requirements.lock
COPY . .
RUN cd ssot/axioms && ln -sf v1.0.1 current && cd /app
RUN python scripts/verify_integrity.py && python scripts/verify_axiom_consistency.py
EXPOSE 8080
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]