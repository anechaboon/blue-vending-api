# Base image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Set environment
ENV PYTHONPATH=/app

# Install dependencies
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY ./app /app/app
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Default command: wait db -> migrate -> seed -> start uvicorn
CMD ["/bin/sh", "-c", "\
  /app/wait-for-it.sh db:5432 --timeout=30 --strict -- \
  python -m app.core.migrate && \
  python -m app.seeders.run_seed && \
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload \
"]
