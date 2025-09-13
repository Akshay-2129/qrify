# Base image with Python 3.10.11
FROM python:3.10.11

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Start the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
