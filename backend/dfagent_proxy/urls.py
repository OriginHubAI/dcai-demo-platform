from django.urls import re_path

from .views import dfagent_proxy


urlpatterns = [
    re_path(r'^(?P<path>.*)$', dfagent_proxy),
]
