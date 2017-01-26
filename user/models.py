from django.db import models
from django.contrib.auth.models import User;


class UserProfile(models.Model):
    user = models.OneToOneField(User);
    description = models.CharField(default="", max_length=10000);
    city = models.CharField(blank=True, null=True, max_length=1000);
    state = models.CharField(blank=True, null=True, max_length=2);
    phone_number = models.IntegerField(blank=True, null=True);
    filter_is_public = models.BooleanField(default=False);