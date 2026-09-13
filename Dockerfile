# Start from a standard python 3 environment
FROM python:3

# Set the working directory inside the container
WORKDIR /app

# Install Flask
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our application code inside the container
COPY app.py .

EXPOSE 8080

# The command to run when the container starts
CMD ["python", "app.py"]