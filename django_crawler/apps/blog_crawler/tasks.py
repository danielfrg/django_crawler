from celery import task
from django.conf import settings
from apps.blog_crawler import utils
from apps.blog_crawler.models import Blog, Post

import time
import urllib
import readability
from bs4 import BeautifulSoup
from text.blob import TextBlob


@task()
def lowerize(post_id):
    post = Post.objects.get(id=post_id)

    post.cleaned = post.cleaned.lower()
    post.save()


@task()
def word_tokenize(post_id):
    post = Post.objects.get(id=post_id)
    text = TextBlob(post.cleaned)

    post.cleaned = ' '.join(text.words)
    post.save()


@task()
def discover_type(blog_id):
    blog = Blog.objects.get(id=blog_id)

    kind = utils.discover_kind(blog.url)
    blog.kind = kind
    blog.save()


@task()
def discover_feed(blog_id):
    blog = Blog.objects.get(id=blog_id)

    if blog.kind is None:
        kind = utils.discover_kind(blog.url)
        blog.kind = kind
    feed = utils.discover_feed(blog.url, blog.kind)
    blog.feed = feed
    blog.save()


@task()
def crawl(blog_id, limit=10):
    blog = Blog.objects.get(id=blog_id)

    # Readability API
    parser = readability.ParserClient(settings.READABILITY_PARSER_TOKEN)

    # Create and start logger
    logger = utils.create_logger(urllib.quote(blog.url).replace('/', '_'))

    logger.info('------------------------------------------------------------')
    post_list = utils.get_posts(blog.feed, blog.kind, limit=limit)
    n_posts = len(post_list)
    logger.info('{0} ({1})'.format(blog.url, n_posts))
    logger.info('------------------------------------------------------------')

    # Start actual crawl
    for i, (url, date) in enumerate(post_list):
        if len(Post.objects.filter(url=url)) > 0:
            logger.info('{0}/{1} Already exists: {2}'.format(i, n_posts, url))
        else:
            parser_response = parser.get_article_content(url)

            try:
                soup = BeautifulSoup(parser_response.content['content'])
                content = soup.get_text(' ', strip=True)
                post = Post(url=url, content=content, date=date)
                post.save()
            except Exception as e:
                logger.info('{0}/{1} FAIL: {2}'.format(i + 1, n_posts, url))
                logger.info(str(e))
            else:
                logger.info('{0}/{1} OK: {2}'.format(i + 1, n_posts, url))
            time.sleep(3.6)
            # time.sleep((60 * 60) / (len(parsers) * 1000))
