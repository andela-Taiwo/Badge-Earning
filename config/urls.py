from allauth.account.views import ConfirmEmailView, LoginView, SignupView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_auth.registration.views import RegisterView, VerifyEmailView
from rest_framework.authtoken.views import obtain_auth_token

from badge_earning.users.views import (
    CustomLoginView,
    complete_view,
    django_rest_auth_null,
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("badge_earning.users.urls", namespace="users")),
    path('accounts/', include('allauth.urls')),
    path('', include('rest_auth.urls')),
    re_path(r'signup/account-email-verification-sent/', django_rest_auth_null, name='account_email_verification_sent'),
    path('signup/complete/', complete_view, name='account_confirm_complete'),
    path('signup/', include('rest_auth.registration.urls')),
    path('signup/', RegisterView.as_view(), name='custom_signup'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/', ConfirmEmailView.as_view(),
        name='account_confirm_email'),
    path('login/', CustomLoginView.as_view(), name='custom_login'),

    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
