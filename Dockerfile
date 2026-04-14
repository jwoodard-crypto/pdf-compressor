FROM python:3.11-slim

# Install system dependencies for PyMuPDF
RUN apt-get update && apt-get install -y \
    mupdf \
    mupdf-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port (Railway uses PORT env variable)
EXPOSE $PORT

# Run with gunicorn, binding to Railway's PORT
CMD gunicorn --bind 0.0.0.0:$PORT app:app
