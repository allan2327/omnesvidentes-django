#!/bin/sh
cd /code/

python manage.py shell -c 'from newsfetch import tasks; tasks.getAllNews()'
python manage.py shell -c 'from newsfetch import tasks; tasks.buildClassifier()'
python manage.py shell -c 'from newsfetch import tasks; tasks.displayNews("#nebc")'
python manage.py shell -c 'from newsfetch import tasks; tasks.displayNews("#oogc")'
python manage.py shell -c 'from newsfetch import tasks; tasks.displayNews("#oilsands")'
