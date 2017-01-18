from django.db import models
from django.contrib.auth.models import User;


class UserProfile(models.Model):
    user = models.OneToOneField(User);
    description = models.CharField(default="", max_length=10000);