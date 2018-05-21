from django.contrib.auth.models import User;
from django.core.validators import RegexValidator;
from django.db import models;
from django import forms;
from random import randint;
from datetime import datetime;
        
alphanumeric = RegexValidator(r'^[0-9a-zA-Z_]+$', 'Alphanumeric characters only');        
        
class Job(models.Model):
    is_finished = models.BooleanField(default=False);
    title = models.CharField(max_length=100);
    date = models.DateTimeField(auto_now_add=True);
    pledging = models.FloatField(default=0);
    paid = models.FloatField(default=0);
    working = models.PositiveIntegerField(default=0);
    finished = models.PositiveIntegerField(default=0);
    received = models.FloatField(default=0);
    location = models.CharField(null=True, blank=True, max_length=1000);
    latitude = models.FloatField(null=True, blank=True);
    longitude = models.FloatField(null=True, blank=True);
    random_string = models.CharField(default='', max_length=100);
    
    def __str__(self):  
        return self.title;
    
    @classmethod
    def create(cls, user, title, latitude=None, longitude=None, location=''):
        job = Job(
            title = title,
            latitude = latitude,
            longitude = longitude,
            location = location, 
            random_string = cls.createRandomString(),
        );
        return job;
    
    @classmethod
    def createRandomString(cls):
        random_string = '';
        available_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
        for i in range(50):
            index = randint(0, len(available_chars)-1);
            random_char = available_chars[index];
            random_string = random_string + random_char;
        if (Job.objects.filter(random_string=random_string).exists()):
            random_string = createRandomString();
        return random_string;
        
    def check_is_finished(self):
        is_finished = False;
        if ((datetime.now() - self.date.replace(tzinfo=None)).days >= 90):
            is_finished = True;
        else:
            if (self.pledging > 0 and self.pledging <= self.paid and self.working > 0 and self.working == self.finished):
                is_finished = True;
        return is_finished;
    
class Tag(models.Model):
    jobs = models.ManyToManyField(Job);    
    tag = models.CharField(max_length=30, validators=[alphanumeric]);
    
    def __str__(self):
        return self.tag;
    
    @classmethod
    def create(cls, tag):
        tag = Tag(
            tag = tag,
        );
        return tag;