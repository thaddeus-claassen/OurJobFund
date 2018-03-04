from django.db import models;
from job.models import Job, User;

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    
    @classmethod
    def create(cls, user, job):
        notification = Notification(
            user = user, 
            job = job,
        );
        return notification;