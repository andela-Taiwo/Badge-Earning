import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class UUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        abstract = True

        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Skill(UUIDModel):
    pass


class Owner(UUIDModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(
        User,
        related_name="%(class)s_owner",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Badge(UUIDModel):
    users = models.ManyToManyField(
        User,
        related_name="%(class)s_badges",
    )
    badge_icon = models.ImageField(upload_to="badge_image_icons", blank=True, null=True)
    owner = models.ForeignKey(
        Owner, related_name="%(class)s_owner", on_delete=models.CASCADE
    )
    skill = models.ManyToManyField(
        Skill,
        related_name="%(class)s_skills",
    )
