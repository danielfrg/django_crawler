from fabric.api import local


def runserver():
    local('python manage.py runserver')


def runserverplus():
    local('python manage.py runserver_plus')


def runcelerycam():
    local('python manage.py celerycam')


def celery_start_general():
    local('python manage.py celery worker -Q general -E -B -c 1 -l info ')

def celery_start_readability():
    local('python manage.py celery worker -Q readability -E -B -c 1 -l info ')


def migrate_crawler():
    local('python manage.py schemamigration blog_crawler --auto')


def apply_crawler_migration():
    local('python manage.py migrate blog_crawler')
