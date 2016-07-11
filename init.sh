#!/usr/bin/env bash

cd /app

python manage.py migrate

echo "Loading audience data..."
python manage.py load_audience
echo "Audience data loaded succesfully"

echo "Loading segments data..."
python manage.py load_segments
echo "Segments loaded successfully"
