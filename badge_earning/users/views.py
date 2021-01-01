from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from dj_rest_auth.registration.views import SocialConnectView, SocialLoginView
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from badge_earning.api.response import BadgeAPIResponse

from . import services as user_service
from .serializers import MyTokenObtainPairSerializer


# Create your views here.
class UserViewSet(viewsets.ViewSet):
    def update(self, request, **kwargs):
        user_id = kwargs.get("pk")
        user = user_service.update_user(
            data=request.data, requestor=request.user, user_id=user_id
        )
        return BadgeAPIResponse(user)


class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://localhost:8000/app/auth"
    # serializer_class = SocialLoginSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://localhost:8000/app/auth"
    serializer_class = SocialLoginSerializer
