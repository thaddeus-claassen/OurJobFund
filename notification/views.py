from django.shortcuts import render;
from django.contrib.auth.models import User;
from .models import Notification;

def sendNotifications(update):
    users = User.objects.filter(jobuser__job=update.jobuser.job).exclude(email=update.jobuser.user.email);
    for user in users:
        if not user.notification_set.filter(job=update.jobuser.job).exists():
            notification = Notification(user=user, job=update.jobuser.job);
            notification.save();
            