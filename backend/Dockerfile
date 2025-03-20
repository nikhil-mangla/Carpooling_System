# Use a slim Python 3.10 image with amd64 architecture
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Install only essential build tools for psycopg2-binary or other binary dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install daphne

# Copy application code
COPY . .

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Run Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "carpooling_backend.asgi:application"]