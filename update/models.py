from django.db import models;
from jobuser.models import JobUser;

class Update(models.Model):
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    title = models.CharField(max_length=100);
    description = models.CharField(default="", max_length=10000);
    pledge = models.FloatField(default=0);
    request_money = models.FloatField(default=0);
    work_status = models.CharField(default='', max_length=100, blank=True);
    date = models.DateTimeField(auto_now_add=True);
    random_string = models.CharField(max_length=50);
    
class Image(models.Model):
    update = models.ForeignKey(Update, on_delete=models.CASCADE, null=True);
    image = models.ImageField();