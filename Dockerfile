# Set base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Create working directory
WORKDIR /app

# Copy the files from the current directory to /app in the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Open port 80 on the container
EXPOSE 80

# Run the FastAPI application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
