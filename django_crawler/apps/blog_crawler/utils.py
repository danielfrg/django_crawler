# encoding: utf-8
from __future__ import division
import os
import math
import logging
import dateutil
import requests
import feedparser
from bs4 import BeautifulSoup

from django.conf import settings


def is_wordpress(soup):
    meta_tags = soup.find_all('meta', {'name': 'generator'})
    for meta_tag in meta_tags:
        if meta_tag['content'].lower().startswith('wordpress'):
            return True

    css_tags = soup.find_all('link', rel='stylesheet')
    for css_tag in css_tags:
        try:
            if 'wp-content' in css_tag['href'] or 'wp-include' in css_tag['href']:
                return True
        except:
            # Some tags don't have `href`
            pass

    script_tags = soup.find_all('script')
    for script_tag in script_tags:
        try:
            if 'wp-content' in script_tag['src'] or 'wp-include' in script_tag['src']:
                return True
        except:
            # Some tags don't have `src`
            pass
    return False


def is_blogspot(soup):
    feed_tags = soup.find_all('link', rel='service.post')
    for feed_tag in feed_tags:
        try:
            if 'blogger.com/feeds' in feed_tag['href']:
                return True
        except:
            # Some tags don't have `href`
            pass


def discover_kind(url):
    kind = None
    if '.blogger.com' in url or '.blogspot.com' in url:
        kind = 'blogspot'
    elif '.wordpress.com' in url:
        kind = 'wordpress'
    else:
        # kind still is None
        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        if is_wordpress(soup):
            kind = 'wordpress'
        elif is_blogspot(soup):
            kind = 'blogspot'

    return kind


def discover_feed(url, kind=None):
    if kind is None:
        kind = discover_kind(url)
    if url[-1] == '/':
        url = url[:-1]

    if kind == 'blogspot':
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        return soup.find('link', rel='service.post')['href']
    if kind == 'wordpress':
        return url + '/feed/'


def get_posts(feed, kind, limit=1000):
    posts = []
    if kind == 'blogspot':
        feed = feed + '?max-results=%i' % limit
        json_feed = feedparser.parse(feed)
        for entry in json_feed['entries']:
            date = dateutil.parser.parse(entry['published'])
            posts.append((entry['link'], date))
    elif kind == 'wordpress':
        page = 1
        while True and page <= math.ceil(limit / 10):
            url = feed + '?paged=%i' % page
            r = requests.get(url)
            if r.status_code == 200:
                json_feed = feedparser.parse(r.text)
                for entry in json_feed['entries']:
                    if len(posts) < limit:
                        date = dateutil.parser.parse(entry['published'])
                        posts.append((entry['link'], date))
                page += 1
            else:
                break
    return posts


def create_logger(url):
    if not os.path.exists(settings.CRAWLER_LOGS_DIR):
        os.makedirs(settings.CRAWLER_LOGS_DIR)

    fname = settings.CRAWLER_LOG_FILE_NAME.format(url)
    fname = os.path.join(settings.CRAWLER_LOGS_DIR, fname)

    logger = logging.getLogger('crawler %s' % url)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(fname)
    f = logging.Formatter(settings.CRAWLER_LOG_FORMAT)
    handler.setFormatter(f)
    logger.addHandler(handler)
    return logger
