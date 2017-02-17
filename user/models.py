from django.db import models;
from django.contrib.auth.models import User;
from job.models import Job;

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE);
    description = models.CharField(default="", max_length=10000);
    city = models.CharField(blank=True, max_length=1000);
    state = models.CharField(blank=True, max_length=2);
    phone_number = models.IntegerField(blank=True, null=True);
    filter_is_public = models.BooleanField(default=False); 

class UserMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="senders");
    message = models.CharField(max_length=10000);
    date_sent = models.DateTimeField(auto_now_add=True);
    date_read = models.DateTimeField(blank=True, null=True, editable=False);
    
class PledgeJob(models.Model):
    pledger = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    date_pledged = models.DateTimeField(auto_now_add=True);
    amount_pledged = models.IntegerField(editable=False, null=True, blank=True);
    amount_paid = models.IntegerField(default=0, null=True, blank=True);
    
class WorkJob(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE);
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    date_joined = models.DateTimeField(auto_now_add=True);
    is_finished = models.BooleanField(default=False);
    amount_of_money_asking_for = models.IntegerField(editable=False, null=True, blank=True);
    total_comments = models.IntegerField(default=0);
    
    def __str__(self):
        return self.worker.username + " : " + self.job.name;

class WorkJobUpdate(models.Model):
    workjob = models.ForeignKey(WorkJob, on_delete=models.CASCADE);
    title = models.CharField(max_length=100, default="");
    updated = models.DateTimeField(auto_now_add=True);
    description = models.CharField(max_length=10000);
    has_active_complaint = models.BooleanField(default=False);
    num_complaints = models.IntegerField(default=0);
    
class ImageUpload(models.Model):
    workJobUpdate = models.ForeignKey(WorkJobUpdate, on_delete=models.CASCADE, null=True);
    image = models.ImageField();
    
class Comment(models.Model):
    workJobUpdate = models.ForeignKey(WorkJobUpdate, on_delete=models.CASCADE, null=True);
    super_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True);
    description = models.TextField(null=True, blank=True);

class UserNotification(models.Model):
    PLEDGE_JOB_UPDATE = 'PU';
    WORK_JOB_UPDATE = 'WU';
    COMMENT = 'CO';
    ASKING_FOR_MONEY = 'MO';
    MESSAGE = 'ME';
    NOTIFICATION_CHOICES = (
        (PLEDGE_JOB_UPDATE, 'Pledge Job Update'),
        (WORK_JOB_UPDATE, 'Work Job Update'),
        (COMMENT, 'Comment'),
        (ASKING_FOR_MONEY, 'Asking For Money'),
        (MESSAGE, 'Message'),
    );
    user = models.OneToOneField(User, on_delete=models.CASCADE);
    read = models.BooleanField(default=False);
    date_read = models.DateTimeField(blank=True, null=True);
    type = models.CharField(max_length=2, choices=NOTIFICATION_CHOICES);
    pledge_job_update = models.OneToOneField(WorkJobUpdate, blank=True, null=True, related_name='pledge_job_update');
    work_job_update = models.OneToOneField(WorkJobUpdate, blank=True, null=True, related_name='work_job_update');
    comment = models.OneToOneField(Comment, blank=True, null=True);
    message = models.OneToOneField(UserMessage, blank=True, null=True);











    