# Use the official Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /chall

COPY . .

# Installing Flask
RUN pip install Flask

# Set environment vars
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=2026

# Expose the port that the chall will run on
EXPOSE 2026

# Run the chall
CMD ["flask", "run", "--host=0.0.0.0"]
