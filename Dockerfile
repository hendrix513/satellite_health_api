# Use the official Python image as base
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code to the container
COPY . .

# Expose port 5000
#EXPOSE 5000

# Command to run the Flask application
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]