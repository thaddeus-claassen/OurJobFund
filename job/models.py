from django.db import models;   
from django import forms;
from django.contrib.auth.models import User;
from django.core.validators import RegexValidator; 
        
alphanumeric = RegexValidator(r'^[0-9a-zA-Z\s]+$', 'Alphanumeric characters only');        
        
class Job(models.Model):
    is_finished = models.BooleanField(default=False);
    name = models.CharField(max_length=100, validators=[alphanumeric]);
    creation_date = models.DateField(auto_now_add=True);
    creation_datetime = models.DateTimeField(auto_now_add=True);
    pledged = models.PositiveIntegerField(default=0);
    paid = models.PositiveIntegerField(default=0);
    workers = models.PositiveIntegerField(default=0);
    finished = models.PositiveIntegerField(default=0);
    location = models.CharField(null=True, blank=True, max_length=1000);
    latitude = models.FloatField(null=True, blank=True);
    longitude = models.FloatField(null=True, blank=True);
    description = models.CharField(default='', max_length=10000, null=True, blank=True);
    created_by = models.ForeignKey(User, null=True);
    random_string = models.CharField(default='', max_length=100);
    
    def __str__(self):  
        return self.name;

class Tag(models.Model):
    jobs = models.ManyToManyField(Job);    
    tag = models.CharField(max_length=30, validators=[alphanumeric]);

    def __str__(self):
        return self.tag;

class Image(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True);
    image = models.ImageField(); 

