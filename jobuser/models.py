from django.db import models;
from job.models import Job;
from django.contrib.auth.models import User;
from datetime import datetime;

class JobUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    amount_pledged = models.FloatField(default=0);
    amount_paid = models.FloatField(default=0);
    oldest_work_date = models.DateTimeField(default=None, null=True, blank=True);
    newest_finish_date = models.DateTimeField(default=None, null=True, blank=True);
    amount_received = models.FloatField(default=0);

class Pledge(models.Model):
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    amount = models.FloatField(null=True, blank=True);
    date = models.DateTimeField(auto_now_add=True);

class Pay(models.Model):    
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    amount = models.FloatField(editable=False, null=True, blank=True);
    receiver = models.ForeignKey(User, on_delete=models.CASCADE);
    date = models.DateTimeField(auto_now_add=True);

class Work(models.Model):    
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    date =  models.DateTimeField(auto_now_add=True);
    
class Finish(models.Model):
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    date =  models.DateTimeField(auto_now_add=True);
