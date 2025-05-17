# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
