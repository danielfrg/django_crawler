from fabric.api import local


def runserver():
    local('python manage.py runserver')


def runserverplus():
    local('python manage.py runserver_plus')


def runceleryworker():
    local('python manage.py celery worker --loglevel=info -E -B')
    #python manage.py celery worker --loglevel=info -E -B -Q crawl -c 1


def migrate_crawler():
    local('python manage.py schemamigration blog_crawler --auto')


def apply_crawler_migration():
    local('python manage.py migrate blog_crawler')
