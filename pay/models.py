from django.db import models;   
from django import forms;
from django.contrib.auth.models import User;
from jobuser.models import JobUser;
    
class Pay(models.Model):
    sender_jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE, related_name='sender_jobuser', null=True, blank=True);
    receiver_jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE, related_name='receiver_jobuser', null=True, blank=True);
    type = models.CharField(default='Other', choices=(('Other', 'Other'), ('Credit/Debit', 'Credit/Debit')), max_length=15);
    verified = models.BooleanField(default=False);
    amount = models.FloatField(editable=False, null=True, blank=True);
    date = models.DateTimeField(auto_now_add=True, null=True);
    
    @classmethod
    def create(cls, sender_jobuser, receiver_jobuser, type, amount):
        pay = Pay(
            sender_jobuser = sender_jobuser,
            receiver_jobuser = receiver_jobuser,
            type = type,
            verified = cls.get_verified(type=type),
            amount = amount,
        );
        return pay;
    
    @classmethod
    def get_verified(cls, type):
        verified;
        if (type == 'Credit/Debit'):
            verified = True;
        else:
            verified = False;
        return verified;