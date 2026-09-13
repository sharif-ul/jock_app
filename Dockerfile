# Start from a standard python 3 environment
FROM python:3

# Set the working directory inside the container
WORKDIR /app

# Install Flask
RUN pip install Flask

# Copy our application code inside the container
COPY . .

# The command to run when the container starts
CMD ["python", "app.py"]