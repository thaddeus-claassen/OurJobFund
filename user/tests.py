from django.test import TestCase;
from .models import User, Profile;
from annoying.functions import get_object_or_None;

class UserTestCase(TestCase):
    
    def setUp(self):
        user = User(username="toadyisgroady", email="toad@toad.com", first_name="toady", last_name="meister");
        user.save();
        
    def test_user(self):
        user = get_object_or_None(User, username="toadyisgroady");
        self.assertIsNotNone(user);
