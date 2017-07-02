from django.db import models;
from django.contrib.auth.models import User;
from job.models import Job;
from django.urls import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE);
    description = models.CharField(default="Email: ", max_length=10000);
    stripe_account_id = models.IntegerField(null=True, blank=True);
    
    def get_absolute_url(self):
        return reverse("user.views.detail", args=[self.random_string]);
        
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    