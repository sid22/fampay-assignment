# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /app

ENV ENVIRONMENT prod
# Copy the current directory contents into the container at /app
COPY . /app

WORKDIR src/

ENTRYPOINT ["./entrypoint.sh"]
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]
