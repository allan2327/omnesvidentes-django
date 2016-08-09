#!/bin/sh
cd /code/

python manage.py shell -c 'from newsfetch import tasks; tasks.getAllNews()'
python manage.py shell -c 'from newsfetch import tasks; tasks.buildClassifier()'
python manage.py shell -c 'from newsfetch import tasks; tasks.displayNews("Oil Sands")'
