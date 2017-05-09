# from __future__ import absolute_import
# import os
# from celery import Celery
# from django.conf import settings
#
# # def get_installed_apps():
# #     installed_apps = []
# #     for django_app in settings.INSTALLED_APPS:
# #         if not django_app.startswith('django.'):
# #             application = os.path.join(settings.BASE_DIR.rsplit('\\', 1)[0], django_app)
# #             installed_apps.append(application)
# #         else:
# #             installed_apps.append(django_app)
# #     return installed_apps
#
#
# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
#
# app = Celery('django_rest')
#
# # Using a string here means the worker will not have to
# # pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)