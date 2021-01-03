from rest_framework.generics import get_object_or_404

from .models import User
from .serializers import UserSerializer


def update_user(requestor, user_id, data):
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user, data=data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    # print(dir(serializer.data))
    return serializer.data
