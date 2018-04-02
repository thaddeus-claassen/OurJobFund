from django.db import models;
from job.models import Job;
from django.contrib.auth.models import User;
from datetime import datetime;

class JobUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    pledging = models.FloatField(default=0, null=True, blank=True);
    paid = models.FloatField(default=0, null=True, blank=True);
    work_status = models.CharField(default='', max_length=100, null=True, blank=True);
    received = models.FloatField(default=0, null=True, blank=True);
    
    @classmethod
    def create(cls, user, job, pledging=0, paid=0, work_status='', received=0):
        jobuser = JobUser(
            user = user,
            job = job,
            pledging = pledging,
            paid = paid,
            work_status = work_status,
            received = received,
        );
        return jobuser;