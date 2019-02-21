from django.contrib.auth.models import User;
from django.shortcuts import render;
from .models import Notification;

def sendNotifications(jobuser):
    users = User.objects.filter(jobuser__job=jobuser.job).exclude(email=jobuser.user.email);
    for user in users:
        sendNotification(user, jobuser.job);
            
def sendNotification(user, job):
    if (not user.notification_set.filter(job=job).exists()):
        notification = Notification.create(user=user, job=job);
        notification.save();