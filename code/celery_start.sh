#!/bin/sh
celery multi start w1 -A omnesvidentes -l info
#celery  multi restart w1 -A omnesvidentes -l info
celery multi stopwait w1 -A omnesvidentes -l info
