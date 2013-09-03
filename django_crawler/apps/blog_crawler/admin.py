from django.contrib import admin
from models import Blog, Post
from apps.blog_crawler import tasks


class BlogAdmin(admin.ModelAdmin):
    list_display = ['url', 'kind', 'feed', 'last_crawl']
    ordering = ['url']
    actions = ['discover_type', 'discover_feed', 'crawl']

    def discover_type(self, request, queryset):
        for blog in queryset:
            tasks.discover_type.delay(blog.id)
        self.message_user(request, 'Task(s) created')

    def discover_feed(self, request, queryset):
        for blog in queryset:
            tasks.discover_feed.delay(blog.id)
        self.message_user(request, 'Task(s) created')

    def crawl(self, request, queryset):
        for blog in queryset:
            tasks.crawl.delay(blog.id)
        self.message_user(request, 'Task(s) created')

    discover_type.short_description = 'Discover the type of the blog(s)'
    discover_feed.short_description = 'Discover the feed of the blog(s)'
    crawl.short_description = 'Crawls the selected blog(s)'


class PostAdmin(admin.ModelAdmin):
    list_display = ['url', 'date']
    actions = ['copy', 'word_tokenize', 'lowerize']

    def copy(self, request, queryset):
        for post in queryset:
            post.cleaned = post.content
            post.save()
        self.message_user(request, 'Content copied')

    def word_tokenize(self, request, queryset):
        for post in queryset:
            tasks.word_tokenize.delay(post.id)
        self.message_user(request, 'Task(s) created')

    def lowerize(self, request, queryset):
        for post in queryset:
            tasks.lowerize.delay(post.id)
        self.message_user(request, 'Task(s) created')

    copy.short_description = 'Copy the crawled content to cleaned'
    word_tokenize.short_description = 'Tockenize by words'
    lowerize.short_description = 'Lower-case the cleaned content'

admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
