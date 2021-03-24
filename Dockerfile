# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /app

ENV ENVIRONMENT prod
# Copy the current directory contents into the container at /app
COPY . /app

WORKDIR src/

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

RUN pip install --upgrade pip && pip install -r ../requirements.txt


# ENTRYPOINT ["./entrypoint.sh"]
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]
