from django.db import models;
from django.contrib.auth.models import User;
from job.models import Job;
from django.urls import reverse;
from django.core.validators import RegexValidator; 
from annoying.fields import AutoOneToOneField;
from .choices import STATES;
import datetime, pytz;

alphabetic = RegexValidator(r'^[a-zA-Z\s]+$', 'Alphabetic characters only');   

class UserProfile(models.Model):
    user = AutoOneToOneField(User, primary_key=True);
    type_of_account = models.CharField(default="personal", max_length=10);
    description = models.CharField(default='', max_length=10000, blank=True);
    city = models.CharField(default='', max_length=100, blank=True);
    state = models.CharField(default='', max_length=2, choices=STATES);
    occupation = models.CharField(default='', max_length=100, blank=True);
    education = models.CharField(default='', max_length=100, blank=True);
    contact = models.CharField(default='', max_length=100, blank=True);
    last_time_name_was_changed = models.DateTimeField(default=pytz.utc.localize(datetime.datetime(2000, 1, 1)));
    preferred_payment = models.CharField(default="N/A", max_length=6);
    stripe_account_id = models.CharField(null=True, blank=True, max_length=100);
    
    def get_absolute_url(self):
        return reverse("user.views.detail", args=[self.random_string]);
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
