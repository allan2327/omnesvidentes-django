from django.shortcuts import render
from django.http import HttpResponse
from . import models

def index(request):
    return HttpResponse("Hello, world. You're at the newsfetch index.")

def news_listing(request):
    """A view of all news items."""
    newsitems = models.NewsItem.objects.all()
    return render(request, 'newsfetch/news_listing.html', {'newsitems': newsitems})
