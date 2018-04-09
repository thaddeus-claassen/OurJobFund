from django.test import TestCase;
from jobuser.models import Job, User, JobUser;
from .models import Update;
from annoying.functions import get_object_or_None;

class UpdateTestCase(TestCase):
    
    def setUp(self):
        user = User(username="user_in_update", email="user@user.com");
        user.save();
        job = Job.create(title="job_in_update");
        job.save();
        jobuser = JobUser.create(user=user, job=job);
        jobuser.save();
        update = Update.create(jobuser, comment="zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP,./;'[]\"\\<>?L:{}|1234567890`-=~!@#$^&*()_+");
        update.save();
        
    def test_jobuser(self):
        user = get_object_or_None(User, username="user_in_update");
        job = get_object_or_None(Job, title="job_in_update");
        jobuser = get_object_or_None(JobUser, user=user, job=job);
        update = get_object_or_None(Update, jobuser=jobuser);
        self.assertIsNotNone(update);