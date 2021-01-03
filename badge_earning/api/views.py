from django.contrib.auth import get_user_model

# from rest_framework import status
# from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin

# from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# from users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    pass
