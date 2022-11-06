from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


class User(AbstractUser):
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    image = models.ImageField(
        upload_to="images/",
        blank=True,
    )
    thumbnail = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[Thumbnail(300, 400)],
        format="JPEG",
    )
    status = models.CharField(max_length=100, blank=True)
