FROM python:3.11-slim

# Create and set working directory
RUN mkdir /app && chmod 777 /app
WORKDIR /app

# Set non-interactive frontend for apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt -qq update && apt -qq install -y git python3 python3-pip ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port for Render health checks
EXPOSE $PORT

# Run the web server + bot
CMD ["python3", "app.py"]
