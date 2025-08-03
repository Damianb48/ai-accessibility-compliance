FROM python:3.10-slim AS base

LABEL maintainer="AI‑Powered Accessibility Compliance"

WORKDIR /app

# Install system dependencies if needed (e.g. for headless Chrome)
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Copy backend source
COPY app/ ./app/
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create reports directory ahead of time
RUN mkdir -p data/reports

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
