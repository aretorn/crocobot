# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# If you have any dependencies, create a requirements.txt file and copy it into the container
# Example: COPY requirements.txt /app/requirements.txt
# Then, install the dependencies using pip:
# RUN pip install -r requirements.txt

# Run script.py when the container launches
RUN python3 --version
RUN python3 -m pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
CMD ["python3", "cbotdock.py"]