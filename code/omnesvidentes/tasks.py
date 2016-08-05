from __future__ import absolute_import
from omnesvidentes.celery import app

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
