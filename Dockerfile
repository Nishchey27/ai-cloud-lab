# Use a lightweight Python 3.9 image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory (including analyze_data.py) into the container
COPY . .

# Specify the command to run when the container starts
# This will execute the analyze_data.py script with a placeholder for the file path
CMD ["python", "analyze_data.py"]