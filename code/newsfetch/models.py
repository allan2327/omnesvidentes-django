from __future__ import unicode_literals

from django.db import models

class Fetcher(models.Model):
    fetcher_name = models.CharField(max_length=200)
    fetcher_desc = models.CharField(max_length=400)
    def __str__(self):
        return self.fetcher_name

class Topic(models.Model):
    fetcher = models.ForeignKey(Fetcher, on_delete=models.CASCADE)
    query_text = models.CharField(max_length=200)
    def __str__(self):
        return self.query_text

class NewsItem(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    content_snippet = models.CharField(max_length=200)
    link = models.CharField(max_length=400)
    source = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    md5hash = models.CharField(max_length=200)
    updated = models.DateField(auto_now=True)
    def __str__(self):
        return self.title
