from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .v1 import urls

router = DefaultRouter()


urlpatterns = [
    path("v1/", include(urls)),
]

if settings.DEBUG:
    router = SimpleRouter()
    import debug_toolbar

    urlpatterns += [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ]
urlpatterns += router.urls
