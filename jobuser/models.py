from django.db import models;
from job.models import Job;
from django.contrib.auth.models import User;

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
    amount_of_money_asking_for = models.IntegerField(null=True, blank=True);
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
    
class Comment(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE);
    commenter = models.ForeignKey(User, on_delete=models.CASCADE);
    is_complaint = models.BooleanField(default=False);
    has_been_nullified = models.BooleanField(default=False);
    update = models.ForeignKey(WorkJobUpdate, on_delete=models.CASCADE, null=True);
    super_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True);
    commented = models.DateTimeField(auto_now_add=True, null=True);
    description = models.TextField(null=True, blank=True);
    
class ImageUpload(models.Model):
    workJobUpdate = models.ForeignKey(WorkJobUpdate, on_delete=models.CASCADE, null=True);
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True);
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, null=True);
    image = models.ImageField();
    
class WorkNotification(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE);
    is_update = models.BooleanField(default=False);
    update = models.ForeignKey(WorkJobUpdate, blank=True, null=True);
    is_comment = models.BooleanField(default=False);
    comment = models.ForeignKey(Comment, blank=True, null=True);
    date_sent = models.DateTimeField(auto_now_add=True, editable=False);
    date_viewed = models.DateTimeField(blank=True, null=True);
    date_read = models.DateTimeField(blank=True, null=True);
    
class PledgeNotification(models.Model):
    pledger = models.ForeignKey(User, on_delete=models.CASCADE);
    is_money_request = models.BooleanField(default=False);
    jo_pk = models.IntegerField(blank=True, null=True);
    is_update = models.BooleanField(default=False);
    update = models.ForeignKey(WorkJobUpdate, on_delete=models.CASCADE, blank=True, null=True);
    is_comment = models.BooleanField(default=False);
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True);
    date_sent = models.DateTimeField(auto_now_add=True, editable=False);
    date_viewed = models.DateTimeField(blank=True, null=True);
    date_read = models.DateTimeField(blank=True, null=True);
    


    
    
    
    
    
    
    
