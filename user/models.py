from django.db import models;
from django.contrib.auth.models import User;
from django.urls import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE);
    description = models.CharField(default="Email: ", max_length=10000);
    
    def get_absolute_url(self):
        return reverse("user.views.detail", args=[self.random_string]);
    