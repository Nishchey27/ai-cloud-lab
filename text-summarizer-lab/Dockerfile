# Use the same base Python image for consistency
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the summarizer script into the container
COPY summarize_text.py .

# The default command is not strictly needed since we specify it in the 'docker run' command,
# but it's good practice for documentation.
CMD ["python", "summarize_text.py"]