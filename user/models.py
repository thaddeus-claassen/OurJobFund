from django.db import models;
from django.contrib.auth.models import User;
from django.urls import reverse
from jobuser.models import WorkJobUpdate, Comment;

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE);
    photo = models.ImageField(default=None);
    description = models.CharField(default="Email: ", max_length=10000);
    random_string = models.CharField(default="", max_length=20);
    
    def get_absolute_url(self):
        return reverse("user.views.detail", args=[self.random_string]);
    