# Use a Python 3.12 base image
FROM python:3.12-slim

# Ensure stdout and stderr are unbuffered
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the port
EXPOSE 8000

# Create directories for static files
RUN mkdir -p /app/staticfiles /app/media

# Make sure the static directory exists and has proper permissions
RUN chmod -R 755 /app/staticfiles

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]