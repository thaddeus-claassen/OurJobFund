from django.db import models;
from django.contrib.auth.models import User;
from job.models import Job;
from django.urls import reverse;
from django.core.validators import RegexValidator; 
from annoying.fields import AutoOneToOneField;
from .choices import STATES;
import datetime, pytz;

alphabetic = RegexValidator(r'^[a-zA-Z\s]+$', 'Alphabetic characters only');

class Profile(models.Model):
    user = AutoOneToOneField(User, primary_key=True, on_delete=models.CASCADE);
    type_of_account = models.CharField(default="personal", max_length=10);
    description = models.CharField(default='', max_length=10000, blank=True);
    location = models.CharField(default='', max_length=100, blank=True);
    occupation = models.CharField(default='', max_length=100, blank=True);
    education = models.CharField(default='', max_length=100, blank=True);
    contact = models.CharField(default='', max_length=100, blank=True);
    last_time_username_was_changed = models.DateTimeField(default=pytz.utc.localize(datetime.datetime(2000, 1, 1)));
    stripe_account_id = models.CharField(default='', null=True, blank=True, max_length=100);
    random_string = models.CharField(max_length=100);
    
    def get_absolute_url(self):
        return reverse("user.views.detail", args=[self.random_string]);
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
