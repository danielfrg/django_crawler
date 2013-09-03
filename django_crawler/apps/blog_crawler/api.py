from tastypie.resources import ModelResource
from apps.blog_crawler.models import Blog, Post


class BlogResource(ModelResource):
    class Meta:
        queryset = Blog.objects.all()
        resource_name = 'blog'


class PostResource(ModelResource):
    class Meta:
        queryset = Post.objects.all()
        resource_name = 'post'
