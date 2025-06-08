# Use Playwright's official Python base image with all browsers preinstalled
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies early to speed up rebuilds
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the app files
COPY . .

# Install Playwright dependencies and browsers (if not already)
RUN playwright install --with-deps

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app (change `app:app` if your main file or app instance is named differently)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
