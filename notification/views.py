from django.contrib.auth.models import User;
from django.shortcuts import render;
from .models import Notification;

def sendNotifications(jobuser):
    users = User.objects.filter(jobuser__job=jobuser.job).exclude(email=jobuser.user.email);
    for user in users:
        if not user.notification_set.filter(job=jobuser.job).exists():
            notification = Notification.create(user=user, job=jobuser.job);
            notification.save();
            