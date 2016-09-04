from django.db import models

# class Table(models.Model):

class Job(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add='True')
    last_time_worked_on = models.DateTimeField(auto_now_add='True')
    money_pledged = models.FloatField(default = '0.0')
    num_people_doing_job = models.IntegerField(default = '0')

    def __str__(self):
        return self.name

