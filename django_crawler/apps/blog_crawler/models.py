from django.db import models


class Blog(models.Model):
    url = models.CharField(max_length=50)
    BLOG_TYPES = (
        ('none', 'General'),
        ('wordpress', 'Wordpress'),
        ('blogspot', 'Blogspot'),
    )
    kind = models.CharField(max_length=20, choices=BLOG_TYPES, default='none', null=True)
    feed = models.CharField(max_length=200, blank=True, null=True)
    last_crawl = models.DateTimeField('Last crawl', blank=True, null=True)


class Post(models.Model):
    blog = models.ForeignKey('Blog')
    url = models.CharField(max_length=200)
    content = models.TextField(max_length=2000, blank=True, null=True)
    cleaned = models.TextField(max_length=2000, blank=True, null=True)
    date = models.DateTimeField('date published', blank=True, null=True)
