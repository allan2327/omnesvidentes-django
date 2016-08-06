from __future__ import unicode_literals
from django.db import models
import hashlib

from django.contrib.contenttypes.fields import GenericRelation

class Fetcher(models.Model):
    fetcher_name = models.CharField(max_length=200)
    fetcher_desc = models.CharField(max_length=400)
    def __str__(self):
        return self.fetcher_name

class Category(models.Model):
    fetcher = models.ForeignKey(Fetcher, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)
    category_desc = models.CharField(max_length=400)
    def __str__(self):
        return self.category_name
    def getFetcher(self):
        return self.fetcher

class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    query_text = models.CharField(max_length=200)
    def __str__(self):
        return self.query_text
    def getCategory(self):
        return self.category

class NewsItem(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    newscategory = models.CharField(max_length=200)
    content_snippet = models.CharField(max_length=1000)
    link = models.CharField(max_length=400)
    source = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    md5hash = models.CharField(max_length=200)
    date = models.DateTimeField()
    updated = models.DateField(auto_now=True)
    rating = models.DecimalField(max_digits=3,decimal_places=1,null=True, blank=True)
    def __str__(self):
        return self.title
