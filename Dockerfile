# Stage 1: Base image with Python 3.12 slim
FROM python:3.12-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# Install OS dependencies required for Firefox
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl gnupg ca-certificates \
    libgtk-3-0 libdbus-glib-1-2 libasound2 libxshmfence1 libxss1 libnss3 \
    fonts-liberation libatk-bridge2.0-0 libatk1.0-0 libcups2 libxcomposite1 \
    libxrandr2 libxdamage1 libx11-xcb1 libgbm-dev xdg-utils libdrm2 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && pip install playwright && playwright install firefox

# Create and set work directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python requirements
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port used by Uvicorn
EXPOSE 8000

# Use a non-root user for better security (optional)
# RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
# USER appuser

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
