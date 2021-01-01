from allauth.account.signals import user_signed_up
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, **fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = fields.pop("email")
        password = fields.get("password1")
        if not email:
            raise ValueError("Email address is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **fields):
        fields.setdefault("is_staff", False)
        fields.setdefault("is_superuser", False)

        return self._create_user(**fields)

    def create_superuser(self, **fields):
        fields.setdefault("is_staff", True)
        fields.setdefault("is_superuser", True)

        if fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(**fields)


class User(AbstractUser):
    """Default user for Badge Earning."""

    #: First and last name do not cover name patterns around the globe

    username = None
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    class Meta:

        verbose_name_plural = "All Users"

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.USERNAME_FIELD})


class Profile(models.Model):
    """ User profile model - main user entry object """

    USER_CLIENT = 0
    USER_ADMIN = 1
    USER_MR = 0
    USER_MS = 1
    USER_MRS = 2
    USER_MISS = 3
    USER_DR = 4

    USER_TYPES = (
        (USER_CLIENT, "Client"),
        (USER_ADMIN, "Admin"),
    )

    USER_TITLES = (
        (USER_MR, "Mr."),
        (USER_MS, "Ms."),
        (USER_MRS, "Mrs."),
        (USER_MISS, "Miss."),
        (USER_DR, "Dr."),
    )

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    GENDER_MALE = 1
    GENDER_FEMALE = 2

    title = models.IntegerField(choices=USER_TITLES, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    mobile_phone = models.CharField(max_length=50, null=True, blank=True)
    address_1 = models.CharField(max_length=255, null=True, blank=True)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    address_3 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.IntegerField(choices=USER_TYPES, default=USER_CLIENT)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    profile_picture_name = models.TextField(null=True, blank=True)
    profile_picture_url = models.URLField(null=True, blank=True)
    profile_picture_key = models.TextField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(user_signed_up)
def populate_profile(user, sociallogin=None, **kwars):
    if sociallogin is None:
        return
    if sociallogin.account.provider.lower() == "google":
        user_data = user.socialaccount_set.filter(provider="google")[0]
        user.profile.avatar_url = user_data.get_avatar_url
        user.profile.first_name = user_data.extra_data.get("given_name")
        user.profile.last_name = user_data.extra_data.get("family_name")
        user.profile.save()
