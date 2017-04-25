from django.db import models;
from django.contrib.auth.models import User;
from jobuser.models import WorkJobUpdate, Comment;

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE);
    description = models.CharField(default="", max_length=10000);
    random_string = models.CharField(default="", max_length=20);
    
    
class Messages(models.Model):
    userA = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messagesA");
    userB = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messagesB");
    most_recent_sent = models.DateTimeField(blank=True, null=True);
    
class UserMessage(models.Model):
    twoUsers = models.ForeignKey(Messages, on_delete=models.CASCADE);
    sender = models.CharField(max_length=1000, default="");
    receiver = models.CharField(max_length=1000, default="");
    message = models.CharField(max_length=10000);
    date_sent = models.DateTimeField(auto_now_add=True, editable=False);
    date_viewed = models.DateTimeField(blank=True, null=True);
    date_read = models.DateTimeField(blank=True, null=True);
   

    