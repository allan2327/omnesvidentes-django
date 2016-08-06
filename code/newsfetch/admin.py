from django.contrib import admin

from .models import Fetcher, Category, Topic, NewsItem

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    def get_fetcher_name(self, obj):
        return obj.fetcher.fetcher_name

    list_display = ['category_name', 'get_fetcher_name', ]
    list_filter = ['category_name', 'fetcher']


class TopicAdmin(admin.ModelAdmin):
    model = Topic

    def get_category_name(self, obj):
        return obj.category.category_name
    get_category_name.admin_order_field  = 'category_name'  #Allows column order sorting
    get_category_name.short_description = 'Category'  #Renames column head

    list_display = ['query_text', 'get_category_name', ]
    list_filter = ['query_text', ]

class NewsItemAdmin(admin.ModelAdmin):
    model = NewsItem

    def get_category_name(self, obj):
        return obj.topic.category.category_name
    def get_fetcher_name(self, obj):
        return obj.topic.category.fetcher.fetcher_name

    list_display = ['title', 'source', 'newscategory','get_category_name','get_fetcher_name','date', 'rating']

admin.site.register(Fetcher)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
