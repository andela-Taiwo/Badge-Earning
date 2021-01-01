from allauth.account.adapter import get_adapter
from allauth.account.forms import ResetPasswordForm
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer, UserDetailsSerializer
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from badge_earning.users.models import Profile, User


class PasswordSerializer(PasswordResetSerializer):
    password_reset_form_class = ResetPasswordForm


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password1", "password2")

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"], None, validated_data["password1"]
        )
        return user


class RegisterSerializerCustom(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def get_cleaned_data(self):
        return {
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user


class UserSerializer(UserDetailsSerializer):
    phone = serializers.CharField(source="profile.phone", required=False)
    mobile_phone = serializers.CharField(source="profile.mobile_phone", required=False)
    address_1 = serializers.CharField(source="profile.address_1", required=False)
    address_2 = serializers.CharField(source="profile.address_2", required=False)
    city = serializers.CharField(source="profile.city", required=False)
    zipcode = serializers.CharField(source="profile.zipcode", required=False)
    country = serializers.CharField(source="profile.country", required=False)
    avatar_url = serializers.CharField(source="profile.avatar_url", required=False)
    last_name = serializers.CharField(source="profile.last_name", required=False)
    first_name = serializers.CharField(source="profile.first_name", required=False)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "avatar_url",
            "last_name",
            "first_name",
            "phone",
            "mobile_phone",
            "address_1",
            "address_2",
            "city",
            "zipcode",
            "country",
        )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        phone = profile_data.get("phone")
        mobile_phone = profile_data.get("mobile_phone")
        address_1 = profile_data.get("address_1")
        address_2 = profile_data.get("address_2")
        zipcode = profile_data.get("zipcode")
        city = profile_data.get("city")
        country = profile_data.get("country")
        avatar_url = profile_data.get("avatar_url")
        last_name = profile_data.get("last_name")
        first_name = profile_data.get("first_name")

        instance = super(UserSerializer, self).update(instance, validated_data)

        # get and update user profile
        profile = instance.profile
        if profile_data:
            profile.phone = phone if phone else profile.phone
            profile.mobile_phone = (
                mobile_phone if mobile_phone else profile.mobile_phone
            )
            profile.address_1 = address_1 if address_1 else profile.address_1
            profile.address_2 = address_2 if address_2 else profile.address_2
            profile.zipcode = zipcode if zipcode else profile.zipcode
            profile.city = city if city else profile.city
            profile.country = country if country else profile.country
            profile.last_name = (
                last_name if last_name is not None else profile.last_name
            )
            profile.first_name = (
                first_name if first_name is not None else profile.first_name
            )
            profile.avatar_url = (
                avatar_url if avatar_url is not None else profile.avatar_url
            )
            profile.save()
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = {
            "avatar_url": self.user.profile.avatar_url,
            "first_name": self.user.profile.first_name,
            "last_name": self.user.profile.last_name,
        }

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class ViewProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        field = "__all__"
        exclude = ["created_at"]
        read_only_fields = ["profile_picture"]

    def get_profile_picture(self, Profile):

        if Profile.profile_picture is not None:
            return Profile.profile_picture.values(
                "profile_picture_url", "profile_picture_key"
            )
        return []
