from django.db import models;
from job.models import Job;
from django.contrib.auth.models import User;
from datetime import datetime;

class JobUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    amount_pledged = models.PositiveIntegerField(default=0);
    amount_paid = models.PositiveIntegerField(default=0);
    newest_work_date = models.DateTimeField(default=None, null=True, blank=True);
    newest_finish_date = models.DateTimeField(default=None, null=True, blank=True);
    amount_received = models.PositiveIntegerField(default=0);

class Pledge(models.Model):
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    amount = models.PositiveIntegerField(null=True, blank=True);
    date = models.DateTimeField(auto_now_add=True);

class Pay(models.Model):    
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    amount = models.PositiveIntegerField(editable=False, null=True, blank=True);
    receiver = models.ForeignKey(User, on_delete=models.CASCADE);
    date = models.DateTimeField(auto_now_add=True);

class Work(models.Model):    
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    date =  models.DateTimeField(auto_now_add=True);
    
class Finish(models.Model):
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    date =  models.DateTimeField(auto_now_add=True);
