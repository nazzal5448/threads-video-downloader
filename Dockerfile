# Use the official Python 3.12 slim image
FROM python:3.12-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget curl gnupg ca-certificates \
    fonts-liberation libappindicator3-1 libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 \
    libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 xdg-utils libgbm-dev libxshmfence1 \
    libxss1 libgtk-3-0 libdrm2 --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright and its browsers
RUN pip install --upgrade pip \
    && pip install playwright \
    && playwright install --with-deps

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
