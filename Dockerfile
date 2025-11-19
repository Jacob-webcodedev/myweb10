# Use an official Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy dependency file and install packages
COPY templates/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code
COPY templates/ .

# Copy static and HTML folders
COPY static/ static/
COPY HTML/ HTML/

# Expose the port Flask will run on
EXPOSE 5000

# Start the Flask app
CMD ["python", "main.py"]