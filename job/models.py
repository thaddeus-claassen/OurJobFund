from django.db import models;   
from django.core.urlresolvers import reverse;
from django import forms;
from django.contrib.auth.models import User;
from ckeditor_uploader.fields import RichTextUploadingField;
        
class Job(models.Model):
    is_active = models.BooleanField(default=True);
    is_finished = models.BooleanField(default=True);
    name = models.CharField(max_length=100);                           
    main_editors = models.ManyToManyField(User, related_name="main_editors");
    creation_date = models.DateTimeField(auto_now_add=True);
    num_people_doing_job = models.IntegerField(default=0);
    money_pledged = models.FloatField(default=0.0);      
    money_paid = models.FloatField(default=0.0);
    latitude = models.FloatField(null=True, blank=True);
    longitude = models.FloatField(null=True, blank=True);
    description = RichTextUploadingField(default='', null=True, blank=True);
    
    def __str__(self):  
        return self.name;    

        
class Tag(models.Model):                                            
    tag = models.CharField(max_length=30);                     
    jobs = models.ManyToManyField(Job);

    def __str__(self):
        return self.tag;                                         

