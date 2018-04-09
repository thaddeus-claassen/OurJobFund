from django.test import TestCase;
from .models import Job, User, JobUser;
from annoying.functions import get_object_or_None;

class JobUserTestCase(TestCase):
    
    def setUp(self):
        user = User(username="user_in_jobuser", email="user@user.com");
        user.save();
        job = Job.create(title="job_in_jobuser");
        job.save();
        jobuser = JobUser.create(user=user, job=job, pledging=1234, paid=1234, work_status="Working", received=1234);
        jobuser.save();
        
    def test_jobuser(self):
        user = get_object_or_None(User, username="user_in_jobuser");
        job = get_object_or_None(Job, title="job_in_jobuser");
        jobuser = get_object_or_None(JobUser, user=user, job=job);
        self.assertIsNotNone(jobuser);
        