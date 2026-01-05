# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements from the root to the container
COPY requirements.txt .

# Install dependencies
# Replace your current RUN pip install line with this:
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copy the api folder content into the container
COPY api/ ./api/

# Expose the FastAPI port
EXPOSE 8000

# Directly run Uvicorn with the correct host binding
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]