FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY . .

# Expose port
EXPOSE 80

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
