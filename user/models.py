from django.db import models;
from django.contrib.auth.models import User;
from jobuser.models import WorkJobUpdate, Comment;

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE);
    is_dependent = models.BooleanField(default=False);
    dependent_on = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dependent_on", null=True);
    description = models.CharField(default="", max_length=10000);
    public_first_name = models.BooleanField(default=False);
    public_last_name = models.BooleanField(default=False);
    city = models.CharField(blank=True, max_length=1000);
    public_city = models.BooleanField(default=False);
    state = models.CharField(blank=True, max_length=2);
    public_state = models.BooleanField(default=False);
    public_filter = models.BooleanField(default=False); 
    
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
   

    