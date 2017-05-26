from django.db import models;
from job.models import Job;
from django.contrib.auth.models import User;

class PledgeJob(models.Model):
    pledger = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    date_pledged = models.DateTimeField(auto_now_add=True);
    amount_pledged = models.IntegerField(editable=False, null=True, blank=True);
    amount_paid = models.IntegerField(default=0, null=True, blank=True);
    
class WorkJob(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    date_joined = models.DateTimeField(auto_now_add=True);
    is_finished = models.BooleanField(default=False);
    amount_of_money_asking_for = models.IntegerField(null=True, blank=True);
    total_comments = models.IntegerField(default=0);
    
    def __str__(self):
        return self.worker.username + " : " + self.job.name;
        
class Update(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    updated = models.DateTimeField(auto_now_add=True);
    comment = models.CharField(max_length=100);
    
class ImageUpload(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True);
    image = models.ImageField();
