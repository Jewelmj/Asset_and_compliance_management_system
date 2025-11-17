# Flask API Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api/ /app/api/
COPY database/ /app/database/
COPY models/ /app/models/
COPY services/ /app/services/
COPY mappers/ /app/mappers/

# Create uploads directory
RUN mkdir -p /app/uploads/compliance

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "-m", "api.app"]
