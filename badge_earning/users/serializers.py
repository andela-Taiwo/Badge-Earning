from allauth.account.adapter import get_adapter
from allauth.account.forms import ResetPasswordForm
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer, UserDetailsSerializer
from django.contrib.auth import get_user_model
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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        field = "__all__"
        exclude = ["created_at"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta(UserDetailsSerializer.Meta):
        model = get_user_model()
        fields = ("email", "profile")

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        profile = instance.profile
        if profile_data is not None:
            phone = profile_data.get("phone")
            mobile_phone = profile_data.get("mobile_phone")
            address_1 = profile_data.get("address_1")
            address_2 = profile_data.get("address_2")
            zipcode = profile_data.get("zipcode")
            city = profile_data.get("city")
            country = profile_data.get("country")
            profile_picture_url = profile_data.get("profile_picture_url")
            last_name = profile_data.get("last_name")
            first_name = profile_data.get("first_name")

            profile.phone = phone if phone is not None else profile.phone
            profile.mobile_phone = (
                mobile_phone if mobile_phone is not None else profile.mobile_phone
            )
            profile.address_1 = (
                address_1 if address_1 is not None else profile.address_1
            )
            profile.address_2 = (
                address_2 if address_2 is not None else profile.address_2
            )
            profile.zipcode = zipcode if zipcode is not None else profile.zipcode
            profile.city = city if city is not None else profile.city
            profile.country = country if country is not None else profile.country
            profile.last_name = (
                last_name if last_name is not None else profile.last_name
            )
            profile.first_name = (
                first_name if first_name is not None else profile.first_name
            )
            profile.profile_picture_url = (
                profile_picture_url
                if profile_picture_url is not None
                else profile.profile_picture_url
            )
            profile.save()
        return super().update(instance, validated_data)
        # return super().update(profile, validated_data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = {
            "profile_picture_url": self.user.profile.profile_picture_url,
            "first_name": self.user.profile.first_name,
            "last_name": self.user.profile.last_name,
        }

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class ViewProfileSerializer(serializers.ModelSerializer):
    profile_picture_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        field = "__all__"
        exclude = ["created_at"]
        read_only_fields = ["profile_picture_name"]

    def get_profile_picture_name(self, Profile):

        if Profile.profile_picture_name is not None:
            return Profile.profile_picture_name.values(
                "profile_picture_url", "profile_picture_key"
            )
        return []
