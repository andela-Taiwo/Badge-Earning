from dj_rest_auth.registration.views import (
    RegisterView,
    SocialAccountDisconnectView,
    SocialAccountListView,
)
from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from badge_earning.users.views import (
    GoogleConnect,
    GoogleLogin,
    MyTokenObtainPairView,
    UserViewSet,
)

router = DefaultRouter()

router.register(r"user", UserViewSet, basename="apiv1_users")

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("login/", MyTokenObtainPairView.as_view(), name="account_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", RegisterView.as_view(), name="account_signup"),
    path("google/login/", GoogleLogin.as_view(), name="google_login"),
    path("google/connect/", GoogleConnect.as_view(), name="google_login"),
    path(
        "socialaccounts/", SocialAccountListView.as_view(), name="social_account_list"
    ),
    path(
        "socialaccounts/<int:pk>/disconnect/",
        SocialAccountDisconnectView.as_view(),
        name="social_account_disconnect",
    ),
    url(r"^", include(router.urls)),
]
