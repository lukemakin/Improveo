from django.db import models
import uuid
import os
from django.conf import settings
from django.dispatch import receiver
from .validators import validate_ext
from django.contrib.auth.models import User
# Create your models here.

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{}.{}".format(uuid.uuid4(), ext)
    return os.path.join('uploads/profile/', filename)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.CharField(max_length=220, blank=True)
    profile_picture = models.ImageField(
        blank=True, default='uploads/profile/profile.png', upload_to=get_file_path, validators=[validate_ext])
    website = models.CharField(
        max_length=50, blank=True, null=True, default=None)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.user)
