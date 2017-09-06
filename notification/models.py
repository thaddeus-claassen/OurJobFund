from django.db import models;
from job.models import Job, User;

TYPES = (('UPDATE', 'UPDATE'), ('WORK', 'WORK'), ('FINISH', 'FINISH'), ('PLEDGE', 'PLEDGE'), ('PAY', 'PAY'));

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    type = models.CharField(default="", max_length=6, choices=TYPES, blank=True);