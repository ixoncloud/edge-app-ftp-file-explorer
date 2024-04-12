# Use a lightweight Python image
FROM python:3.11-slim

# Install required system packages for FTP and virtual environment
RUN apt-get update && \
    apt-get install -y gcc libffi-dev libssl-dev libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*  # Clean up

# Create and activate a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Flask and gunicorn within the virtual environment
RUN pip install --no-cache-dir Flask gunicorn

# Set environment variables for FTP configuration
ENV FTP_SERVER=192.168.140.1
ENV FTP_USERNAME=ftpuser
ENV FTP_PASSWORD=ftppassword

# Copy the Flask app and the templates
COPY app.py /app.py
COPY templates /templates

# Expose the port gunicorn will run on
EXPOSE 5090

# Command to run the Flask app with gunicorn using 4 worker processes
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5090", "app:app"]
