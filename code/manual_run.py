#!/bin/sh

python manage.py shell -c 'from newsfetch import tasks; tasks.getAllNews()'
python manage.py shell -c 'from newsfetch import tasks; tasks.buildClassifier()'
