# Base image
FROM python:3.12-slim

# Create app directory
WORKDIR /app

# Install system dependencies (needed for psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements separately so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Port exposed internally (nginx talks to this)
EXPOSE 8000

# Start gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "Flow.wsgi:application"]
