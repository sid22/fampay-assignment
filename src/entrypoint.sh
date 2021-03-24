#!/bin/sh

# Data base migrations
python manage.py migrate

#create cache table
python manage.py createcachetable

# Execute the command passed via args
exec "$@"
