from django.test import TestCase;
from job.models import Job, User;
from .models import Notification;
from annoying.functions import get_object_or_None;

class JobUserTestCase(TestCase):
    
    def setUp(self):
        user = User(username="user_in_notification", email="user@user.com");
        user.save();
        job = Job.create(public=True, title="job_in_notification");
        job.save();
        notification = Notification.create(user=user, job=job);
        notification.save();
        
    def test_jobuser(self):
        user = get_object_or_None(User, username="user_in_notification");
        job = get_object_or_None(Job, title="job_in_notification");
        notification = get_object_or_None(Notification, user=user, job=job);
        self.assertIsNotNone(notification);
        