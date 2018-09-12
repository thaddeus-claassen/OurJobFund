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
    joined = models.DateTimeField(default=datetime.min);
    banned = models.BooleanField(default=False);
    random_string = models.CharField(max_length=50);
    
    @classmethod
    def create(cls, user, job, pledging=0, paid=0, work_status='', received=0):
        jobuser = JobUser(
            user = user,
            job = job,
            pledging = pledging,
            paid = paid,
            work_status = work_status,
            received = received,
            random_string = cls.createRandomString(),
        );
        return jobuser;
        
    @classmethod
    def createRandomString(cls):
        from random import randint;
        random_string = '';
        available_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
        for i in range(50):
            index = randint(0, 61);
            random_char = available_chars[index];
            random_string = random_string + random_char;
        if (JobUser.objects.filter(random_string=random_string).exists()):
            random_string = createRandomString();
        return random_string;
        
    def set_banned(self, value):
        self.banned = value;
        if (not value):
            for mod in self.moderator_set.filter(active=True):
                mod.active = False;
                mod.save();
        
       
class Moderator(models.Model):
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    is_super = models.BooleanField(default=False);
    active = models.BooleanField(default=True);
    date = models.DateTimeField(auto_now_add=True);
    
    @classmethod
    def create(cls, jobuser):
        moderator = Moderator(
            jobuser = jobuser,
        );
        return moderator;
        
    def get_date(self):
        return self.date;
            
    def get_type(self):
        if (self.is_super):
            return "Super Moderator";
        else:
            return "Moderator";
                
    def get_amount(self):
        return "N/A";
        
    def get_to(self):
        return "N/A";
    
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
    confirmed = models.NullBooleanField(default=None);
    
    @classmethod
    def create(cls, jobuser, receiver, amount):
        misc_pay = MiscPay(
            jobuser=jobuser,
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
    def create(cls, jobuser, receiver, amount):
        stripe_pay = StripePay(jobuser=jobuser, receiver=receiver, amount=amount);
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
    #payment_type = models.CharField(choices=(('', '(Please Select your method of receiving payments)'), ('Credit/Debit', 'Credit/Debit'), ('Either', 'Either'), ('Contact Me', 'Contact Me')), max_length=100);
    
    @classmethod
    def create(cls, jobuser):
        work = Work(jobuser=jobuser);
        return work;
        
    def get_type(self):
        return 'Work';
        
    #def get_payment_type(self):
        #return self.payment_type;
    
class Finish(WorkFinish):
    
    @classmethod
    def create(cls, jobuser):
        finish = Finish(jobuser=jobuser);
        return finish;
        
    def get_type(self):
        return 'Finish';