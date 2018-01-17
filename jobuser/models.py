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
    
