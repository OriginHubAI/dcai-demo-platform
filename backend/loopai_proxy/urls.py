from django.urls import re_path
from .views import loopai_proxy

urlpatterns = [
    re_path(r'^(?P<path>.*)$', loopai_proxy),
]
