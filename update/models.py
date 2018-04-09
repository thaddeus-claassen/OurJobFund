from django.db import models;
from jobuser.models import JobUser;
from random import randint;

class Update(models.Model):
    jobuser = models.ForeignKey(JobUser, on_delete=models.CASCADE);
    comment = models.CharField(default="", max_length=10000, blank=True);
    date = models.DateTimeField(auto_now_add=True);
    random_string = models.CharField(max_length=50);
    
    @classmethod
    def create(cls, jobuser, comment):
        update = Update(
            jobuser = jobuser,
            comment = comment,
            random_string = cls.createRandomString(),
        );
        return update;

    @classmethod
    def createRandomString(cls):
        random_string = '';
        available_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
        for i in range(50):
            index = randint(0, 61);
            random_char = available_chars[index];
            random_string = random_string + random_char;
        if (Update.objects.filter(random_string=random_string).exists()):
            random_string = createRandomString();
        return random_string;
    
class Image(models.Model):
    update = models.ForeignKey(Update, on_delete=models.CASCADE, null=True);
    image = models.ImageField();
    
    @classmethod
    def create(cls, update, image):
        image = Image(
            update = update,
            image = image,
        );
        return image;