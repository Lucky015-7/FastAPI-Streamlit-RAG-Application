# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements from the root to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the api folder content into the container
COPY api/ ./api/

# Expose the FastAPI port
EXPOSE 8000

# Command to run the FastAPI server
CMD ["python", "api/main.py"]