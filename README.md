django-crawler
==============

A django blog crawler that uses readability to extract the article form different site.

Uses celery and Django celery to queue tasks.

How to run
----------

The utils queue can be distributed
`python manage.py celery worker -l info -E -B -Q utils -c 1`

The crawl queue needs to be only one for readability API restrictions
`python manage.py celery worker -l info -E -B -Q crawl -c 1 --hostname=crawler`

See and records the celery events
`python manage.py celerycam`

Run django
`python manage.py runserver_plus`

