from django.db import models;   
from django import forms;
from django.contrib.auth.models import User;
from django.core.validators import RegexValidator;
from random import randint;
        
alphanumeric = RegexValidator(r'^[0-9a-zA-Z_]+$', 'Alphanumeric characters only');        
        
class Job(models.Model):
    is_finished = models.BooleanField(default=False);
    name = models.CharField(max_length=100);
    creation_date = models.DateField(auto_now_add=True);
    creation_datetime = models.DateTimeField(auto_now_add=True);
    pledged = models.FloatField(default=0);
    paid = models.FloatField(default=0);
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
        
    def get_absolute_url(self):
        return "/job/%s/" % self.random_string;
        
    @classmethod    
    def create(cls, name, description, created_by, latitude='', longitude='', location=''):
        job = Job(
            name = name,
            latitude = latitude,
            longitude = longitude,
            location = location, 
            description = description,
            created_by = created_by,
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
        
class Image(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True);
    image = models.ImageField();
    
    @classmethod
    def create(cls, job, image):
        image = Image(
            job = job, 
            image = image,
        );
        return image;

