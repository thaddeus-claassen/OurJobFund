from django.test import TestCase;
from .models import Job;
from annoying.functions import get_object_or_None;

class JobTestCase(TestCase):
    
    def setUp(self):
        job = Job.create(title="zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP,./;'[]\"\\<>?L:{}|1234567890`-=~!@#$^&*()_+");
        job.save();
        
    def test_job(self):
        job = get_object_or_None(Job, title="zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP,./;'[]\"\\<>?L:{}|1234567890`-=~!@#$^&*()_+");
        self.assertIsNotNone(job);