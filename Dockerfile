# Use an official Python runtime as a parent image
# FROM python:3.10
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir models

# Download the Whisper model during the build
ENV MODEL_VERSION=CAiRE/SER-wav2vec2-large-xlsr-53-eng-zho-all-age
RUN mkdir -p /app/models && \
    python -c "from transformers import pipeline; pipeline('audio-classification', model='$MODEL_VERSION')"

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the application code into the container
COPY main.py .

# Expose port 8080
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]