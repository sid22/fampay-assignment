#!/bin/sh

# Data base migrations
python manage.py migrate

# Execute the command passed via args
exec "$@"
