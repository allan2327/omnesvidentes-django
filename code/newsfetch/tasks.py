from __future__ import absolute_import
from celery import shared_task
import newsfetch
import gnp.gnp as gnp
import hashlib
import datetime
import re
import parsedatetime

def getNews(q):
    news = gnp.get_google_news_query(q=q)
    stories = news['stories']
    formattedStories = []
    for story in stories:
        story['link'] = story['link'].decode('utf-8')
        story['content_snippet'] = story['content_snippet'].decode('utf-8')
        story['title'] = story['title'].decode('utf-8')
        story['source'] = story['source'].decode('utf-8')
        story['date'] = story['date'].decode('utf-8')
        formattedStories.append(story)
    return formattedStories

@shared_task()
def getAllNews():
    topics = newsfetch.models.Topic.objects.all()
    for topic in topics:
        stories = getNews(q = topic.query_text)
        for story in stories:
            cal = parsedatetime.Calendar()
            temp, status = cal.parse(re.sub('[^A-Za-z0-9 ]+', '', story['date']))
            temp = datetime.datetime(*temp[:6])
            obj = newsfetch.models.NewsItem(topic = topic,newscategory = story['category'],content_snippet = story['content_snippet'],link = story['link'],source = story['source'],title = story['title'], date = temp)
            obj.md5hash = hashlib.md5(obj.link.encode()).hexdigest()
            # Check if hash exists in db before saving (avoid duplicates)!
            if newsfetch.models.NewsItem.objects.filter(md5hash = obj.md5hash, topic = topic).__len__() == 0:
                obj.save()
    return True
