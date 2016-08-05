from __future__ import absolute_import
from celery import shared_task

import gnp.gnp as gnp
import nltk
import codecs
import json

@shared_task
def getNews(q):
    news = gnp.get_google_news_query(q=q)
    stories = news['stories']
    formattedStories = []
    for story in stories:
        story['link'] = story['link'].decode('utf-8')
        story['content_snippet'] = story['content_snippet'].decode('utf-8')
        story['title'] = story['title'].decode('utf-8')
        story['source'] = story['source'].decode('utf-8')
        formattedStories.append(story)
    return formattedStories

@shared_task
def getNewsTopics(topics):
    allStories = []
    for topic in topics:
        allStories.append(getNews(topic))
    return allStories
