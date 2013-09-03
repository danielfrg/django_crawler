from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Tastypie API
from tastypie.api import Api
from apps.blog_crawler.api import BlogResource, PostResource
api = Api(api_name='api')
api.register(BlogResource())
api.register(PostResource())


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^', include(api.urls)),

    # Examples:
    # url(r'^$', 'django_crawler.views.home', name='home'),
    # url(r'^django_crawler/', include('django_crawler.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
