from django.db import models;
from jobuser.models import JobUser;

class Work(models.Model):    
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    status = models.CharField(default='', choices=(('working', 'working'),('finished', 'finished')), max_length=10);
    comment = models.CharField(default='', blank=True, null=True, max_length = 10000);
    date =  models.DateTimeField(auto_now_add=True);
    random_string = models.CharField(default='', max_length=100);
