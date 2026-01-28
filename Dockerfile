# Use a slim version of Python to keep the image size small
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files
# and to ensure logs are sent straight to the terminal (no buffering)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# Install system dependencies
# - libpq-dev & gcc: Required for psycopg2 (Postgres)
# - curl: For health checks
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the Flask app runs on
EXPOSE 8000

# Default command: runs the Flask app
# (Note: We override this in docker-compose for the worker)
CMD ["python", "src/page.py"]