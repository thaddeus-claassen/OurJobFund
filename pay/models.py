from django.db import models;   
from django import forms;
from django.contrib.auth.models import User;
from jobuser.models import JobUser;
    
class Pay(models.Model):    
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    amount = models.FloatField(editable=False, null=True, blank=True);
    receiver = models.ForeignKey(User, on_delete=models.CASCADE);
    date = models.DateTimeField(auto_now_add=True);