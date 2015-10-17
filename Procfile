web: python manage.py deploy; python manage.py runserver
worker: celery -A oj.core.tasks:celery worker
beat: celery -A oj.core.tasks:celery beat
