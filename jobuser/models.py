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
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    date = models.DateTimeField(auto_now_add=True);
      
    class Meta:
        abstract = True;
    
    def get_username(self):
        return self.jobuser.user.username;
        
    def get_from(self):
        return self.get_username();
        
    def get_to(self):
        return 'N/A';

    def get_date(self):
        return self.date;
        
    def get_confirmed(self):
        return 'N/A';
        
class PledgePay(PledgePayWorkFinish):
    amount = models.FloatField(null=True, blank=True);
    
    class Meta:
        abstract = True;
        
    def get_amount(self):
        return self.amount;
    
class Pledge(PledgePay):
    
    @classmethod
    def create(cls, jobuser, amount):
        pledge = Pledge(jobuser=jobuser, amount=amount);
        return pledge;
    
    def get_type(self):
        return 'Pledge';
    
class MiscPay(PledgePay):
    receiver = models.ForeignKey(JobUser, on_delete=models.CASCADE, related_name='misc_pay_receiver');
    confirmed = models.CharField(default="Unconfirmed", choices=(('Unconfirmed', 'Unconfirmed'), ('Confirmed', 'Confirmed'), ('Rejected', 'Rejected')), max_length=100);
    
    @classmethod
    def create(cls, sender, receiver, amount):
        misc_pay = MiscPay(
            jobuser=sender,
            receiver=receiver,
            amount=amount,
        );
        return misc_pay;
    
    def get_to(self):
        return self.receiver.user.username;
        
    def get_confirmed(self):
        return self.confirmed;
    
    def get_type(self):
        return 'Misc. Payment';
    
class StripePay(PledgePay):
    receiver = models.ForeignKey(JobUser, on_delete=models.CASCADE, related_name='stripe_pay_receiver');
    
    @classmethod
    def create(cls, sender, receiver, amount):
        stripe_pay = StripePay(jobuser=sender, receiver=receiver, amount=amount);
        return stripe_pay;
    
    def get_to(self):
        return self.receiver.user.username;
    
    def get_type(self):
        return 'Stripe Payment';
        
class WorkFinish(PledgePayWorkFinish):
    
    class Meta:
        abstract = True;
    
    def get_amount(self):
        return -1;
    
class Work(WorkFinish):
    payment_type = models.CharField(choices=(('', '(Please Select your method of receiving payments)'), ('Credit/Debit', 'Credit/Debit'), ('Either', 'Either'), ('Contact Me', 'Contact Me')), max_length=100);
    
    @classmethod
    def create(cls, jobuser, payment_type):
        work = Work(jobuser=jobuser, payment_type=payment_type);
        return work;
        
    def get_type(self):
        return 'Work';
        
    def get_payment_type(self):
        return self.payment_type;
    
class Finish(WorkFinish):
    
    @classmethod
    def create(cls, jobuser):
        finish = Finish(jobuser=jobuser);
        return finish;
        
    def get_type(self):
        return 'Finish';