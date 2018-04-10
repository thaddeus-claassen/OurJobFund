from django.db import models;
from job.models import Job;
from django.contrib.auth.models import User;
from datetime import datetime;

class JobUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    pledging = models.FloatField(default=0);
    paid = models.FloatField(default=0);
    work_status = models.CharField(default='', max_length=100, null=True, blank=True);
    preferred_payment_method = models.CharField(default='', max_length=100);
    received = models.FloatField(default=0);
    
    @classmethod
    def create(cls, user, job, pledging=0, paid=0, work_status='', received=0):
        jobuser = JobUser(
            user = user,
            job = job,
            pledging = pledging,
            paid = paid,
            work_status = work_status,
            received = received,
        );
        return jobuser;
    
class PledgePayWorkFinish(models.Model):        
    date = models.DateTimeField(auto_now_add=True);
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
      
    class Meta:
        abstract = True;
        
class PledgePay(PledgePayWorkFinish):
    amount = models.FloatField(null=True, blank=True);
    
    class Meta:
        abstract = True;
    
class Pledge(PledgePay):
    
    @classmethod
    def create(cls, jobuser, amount):
        pledge = Pledge(jobuser=jobuser, amount=amount);
        return pledge;
    
class MiscPay(PledgePay):
    verified = models.NullBooleanField(default=None);
    receiver = models.ForeignKey(JobUser, on_delete=models.CASCADE, related_name='misc_pay_receiver');
    
    @classmethod
    def create(cls, sender, receiver, amount):
        misc_pay = MiscPay(jobuser=sender, receiver=receiver, amount=amount);
        return misc_pay;
    
class StripePay(PledgePay):
    receiver = models.ForeignKey(JobUser, on_delete=models.CASCADE, related_name='stripe_pay_receiver');
    
    @classmethod
    def create(cls, sender, receiver, amount):
        stripe_pay = StripePay(jobuser=sender, receiver=receiver, amount=amount);
        return stripe_pay;
    
class Work(PledgePayWorkFinish):
    payment_type = models.CharField(choices=(('', '(Please Select your method of receiving payments)'), ('Credit/Debit', 'Credit/Debit'), ('Either', 'Either'), ('Contact Me', 'Contact Me')), max_length=100);
    
    @classmethod
    def create(cls, jobuser, payment_type):
        work = Work(jobuser=jobuser, payment_type=payment_type);
        return work;
    
class Finish(PledgePayWorkFinish):
    
    @classmethod
    def create(cls, jobuser):
        finish = Finish(jobuser=jobuser);
        return finish;