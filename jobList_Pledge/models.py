from django.db import models;   
from django.core.urlresolvers import reverse;
from django import forms;
        
# Creates a Job database
class Job(models.Model):                                                  
    name = models.CharField(max_length=100);                            # Adds the name of the job as a column to the database   
    creation_date = models.DateTimeField(auto_now_add='True');          # Adds the creation date as a column to the database
    last_time_worked_on = models.DateTimeField(auto_now_add='True');    # Remembers the last time the job was worked as a column
    money_pledged = models.FloatField(default = '0.0');                 # Adds the amount of money pledged as a column
    num_people_doing_job = models.IntegerField(default = '0');          # Adds the number of people who are working on the job as a column
    latitude = models.FloatField(null = True);
    longitude = models.FloatField(null = True);
    description = models.CharField(default="", max_length=10000);
    
    # Defines a toString method
    def __str__(self):  
        return self.name;                                               # Returns the name of the job for the moment



# Create a Tag database
class Hashtag(models.Model):                                            
    hashtag = models.CharField(max_length=30);                              # Adds the tag as a column to the database
    jobs = models.ManyToManyField(Job);

    # Defines a toString method
    def __str__(self):
        return self.hashtag;                                            # Retuns the tag itself
