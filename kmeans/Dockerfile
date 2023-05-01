# Use the official Ubuntu 22.04 image as the base image
FROM ubuntu:22.04

# Update package lists and install Java and Python
RUN apt-get update && apt-get install -y default-jdk python3 python3-pip

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set environment variables
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Start the MQTT subscriber script
CMD ["python3", "kmeans-ads.py"]
