from django.contrib import admin

from .models import Fetcher, Topic, NewsItem

admin.site.register(Fetcher)
admin.site.register(Topic)
