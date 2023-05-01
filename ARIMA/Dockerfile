# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN apt-get update
RUN apt install default-jdk -y

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set environment variables
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3
# ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

# Expose the port that the app will be running on
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "ARIMA.py"]
