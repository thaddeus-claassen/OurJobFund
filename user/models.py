from django.db import models;
from django.contrib.auth.models import User;
from job.models import Job;
from django.urls import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE);
    description = models.CharField(default="Email: ", max_length=10000);
    last_time_name_was_changed = models.DateTimeField(default="2000-01-01");
    stripe_account_id = models.CharField(null=True, blank=True, max_length=100);
    
    def get_absolute_url(self):
        return reverse("user.views.detail", args=[self.random_string]);
        
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    