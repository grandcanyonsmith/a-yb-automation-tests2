# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory condtents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable


# Install necessary browser binaries for Playwright
RUN playwright install-deps

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME YearbookTesting

# Run pytest when the container launches
CMD ["pytest", "tests/legacy/ui_tests/"]
