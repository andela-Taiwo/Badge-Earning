from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).
        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown or not verified, just go on
        - social account's email exists, link social account to existing user
        """
        user_data = sociallogin.account.extra_data
        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing or sociallogin.account.provider.lower() != "google":
            return

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        social_email = user_data.get("email")
        if social_email is None or not user_data.get("verified_email"):
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            email = EmailAddress.objects.get(email__iexact=social_email, verified=True)
            user = email.user
            user.profile.avatar_url = user_data.get("picture")
            user.profile.first_name = user_data.get("given_name")
            user.profile.last_name = user_data.get("family_name")
            user.profile.save()

        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        sociallogin.connect(request, user)
