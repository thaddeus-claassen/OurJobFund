from django.db import models;
from job.models import Job;
from django.contrib.auth.models import User;

class JobUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);

class Pledge(models.Model):
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    amount = models.IntegerField(editable=False, null=True, blank=True);
    date = models.DateTimeField(auto_now_add=True);
    
class Pay(models.Model):    
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    amount = models.IntegerField(editable=False, null=True, blank=True);
    date = models.DateTimeField(auto_now_add=True);

class Work(models.Model):    
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    date =  models.DateTimeField(auto_now_add=True);
    
class Finish(models.Model):
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    date =  models.DateTimeField(auto_now_add=True);

class Update(models.Model):
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    title = models.CharField(max_length=100);
    comment = models.CharField(max_length=1000);
    date = models.DateTimeField(auto_now_add=True);
    
class ImageUpload(models.Model):
    update = models.ForeignKey(Update, on_delete=models.CASCADE, null=True);
    image = models.ImageField();
