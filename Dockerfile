# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment
ENV PYTHONPATH=/app

# Copy and install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app /app/app

# Copy wait-for-it script
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Default command: wait for DB -> migrate -> seed -> start uvicorn
CMD ["/bin/sh", "-c", "\
  /app/wait-for-it.sh db:5432 --timeout=30 --strict -- \
  python -m app.core.migrate && \
  python -m app.seeders.run_seed && \
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload \
"]
