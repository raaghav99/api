# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Additional setup for NLTK
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader punkt

# Expose port 8000 to the outside world
EXPOSE 8000

# Run Gunicorn with 4 worker processes for better performance
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
