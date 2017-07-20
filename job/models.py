from django.db import models;   
from django import forms;
from django.contrib.auth.models import User;
        
class Job(models.Model):
    is_finished = models.BooleanField(default=False);
    name = models.CharField(max_length=100);
    creation_date = models.DateField(auto_now_add=True);
    creation_datetime = models.DateTimeField(auto_now_add=True);
    num_workers = models.IntegerField(default=0);
    money_pledged = models.FloatField(default=0.0);      
    money_paid = models.FloatField(default=0.0);
    location = models.CharField(null=True, blank=True, max_length=1000);
    latitude = models.FloatField(null=True, blank=True);
    longitude = models.FloatField(null=True, blank=True);
    description = models.CharField(default='', max_length=10000, null=True, blank=True);
    random_string = models.CharField(default='', max_length=100);
    
    def __str__(self):  
        return self.name;   

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('job.views.detail', args=[str(self.random_string)])

class Tag(models.Model):                                            
    tag = models.CharField(max_length=30);                     
    jobs = models.ManyToManyField(Job);

    def __str__(self):
        return self.tag;

class Image(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True);
    image = models.ImageField();        

