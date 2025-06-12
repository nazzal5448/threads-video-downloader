# Stage 1: Base image with Python 3.12 slim
FROM python:3.12-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive \
    DEBUG="pw:browser*" \
    PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright

# Install OS dependencies required for Playwright Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl gnupg ca-certificates \
    fonts-liberation libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libxcomposite1 libxrandr2 libxdamage1 libx11-xcb1 libgbm-dev \
    xdg-utils libdrm2 libxshmfence1 libnss3 libxss1 libasound2 \
    libxcomposite1 libxcursor1 libxi6 libxtst6 libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create the playwright browser path directory with correct permissions
RUN mkdir -p /tmp/playwright && chmod -R 777 /tmp/playwright

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install playwright && \
    playwright install --with-deps chromium

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose the port used by Uvicorn
EXPOSE 8000

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
