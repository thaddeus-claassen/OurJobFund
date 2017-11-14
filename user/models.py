from django.db import models;
from django.contrib.auth.models import User;
from job.models import Job;
from django.urls import reverse;
from django.core.validators import RegexValidator; 
from annoying.fields import AutoOneToOneField;
import datetime, pytz;

alphabetic = RegexValidator(r'^[a-zA-Z\s]+$', 'Alphabetic characters only');   

STATES = (
    ('', ''),('AL', 'AL'),('AK', 'AK'),('AZ', 'AZ'),('AR', 'AR'),('CA', 'CA'),('CO', 'CO'),('CT', 'CT'),('DE', 'DE'),('FL', 'FL'),
    ('GA', 'GA'),('HI', 'HI'),('ID', 'ID'),('IL', 'IL'),('IN', 'IN'),('IA', 'IA'),('KS', 'KS'),('KY', 'KY'),('LA', 'LA'),('ME', 'ME'),
    ('MD', 'MD'),('MA', 'MA'),('MI', 'MI'),('MN', 'MN'),('MS', 'MS'),('MO', 'MO'),('MT', 'MT'),('NE', 'NE'),('NV', 'NV'),('NH', 'NH'),
    ('NJ', 'NJ'),('NM', 'NM'),('NY', 'NY'),('NC', 'NC'),('ND', 'ND'),('OH', 'OH'),('OK', 'OK'),('OR', 'OR'),('PA', 'PA'),('RI', 'RI'),
    ('SC', 'SC'),('SD', 'SD'),('TN', 'TN'),('TX', 'TX'),('UT', 'UT'),('VT', 'VT'),('VA', 'VA'),('WA', 'WA'),('WV', 'WV'),('WI', 'WI'),
    ('WY','WY'),('GU', 'GU'),('PR', 'PR'),('VI', 'VI'),
);

class UserProfile(models.Model):
    user = AutoOneToOneField(User, primary_key=True);
    description = models.CharField(max_length=10000, blank=True);
    city = models.CharField(max_length=100, blank=True);
    state = models.CharField(max_length=2, choices=STATES, default='');
    occupation = models.CharField(max_length=100, blank=True);
    education = models.CharField(max_length=100, blank=True);
    last_time_name_was_changed = models.DateTimeField(default=pytz.utc.localize(datetime.datetime(2000, 1, 1)));
    stripe_account_id = models.CharField(null=True, blank=True, max_length=100);
    
    def get_absolute_url(self):
        return reverse("user.views.detail", args=[self.random_string]);
        
class UserInfo(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE);
    title = models.CharField(max_length=20);
    info = models.CharField(max_length=100);
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
