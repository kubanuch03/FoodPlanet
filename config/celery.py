from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# Установите переменную окружения DJANGO_SETTINGS_MODULE, чтобы Celery знал, какие настройки Django использовать.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создайте экземпляр Celery с именем вашего проекта.
celery_app = Celery('config')

# Загрузите настройки из файла настроек Django.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из приложений Django.
celery_app.autodiscover_tasks(related_name='tasks')


# celery_app.conf.beat_schedule = {
#     'delete-expired-cart-items': {
#         'task': 'products.tasks.delete_expired_cart_items',  # Путь к вашей задаче
#         'schedule': crontab(minute='*'),
#     },
# }
