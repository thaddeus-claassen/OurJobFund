from django.db import models;   
from django import forms;
from django.contrib.auth.models import User;
from jobuser.models import JobUser;
    
class Pay(models.Model):
    sender_jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE, related_name='sender_jobuser', null=True, blank=True);
    receiver_jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE, related_name='receiver_jobuser', null=True, blank=True);
    type = models.CharField(choices=(('Other', 'Other'), ('Credit', 'Credit')), max_length=10);
    amount = models.FloatField(editable=False, null=True, blank=True);
    date = models.DateTimeField(auto_now_add=True);