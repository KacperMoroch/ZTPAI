# Use the official Python image
FROM python:3.12-slim
# Set environment variables to avoid interactive prompts during builds
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# Set working directory inside the container
WORKDIR /app
# Copy the requirements file
COPY requirements.txt /app/
# Install system dependencies and Python dependencies
RUN apt-get update && apt-get install -y \
gcc \
libpq-dev \
&& pip install --upgrade pip \
&& pip install -r requirements.txt \
&& apt-get clean && rm -rf /var/lib/apt/lists/*
# Copy the rest of the application code
COPY . /app/
# Expose the port Django will run on
EXPOSE 8000