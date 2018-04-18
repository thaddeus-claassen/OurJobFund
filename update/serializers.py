from rest_framework import serializers;
from .models import Update;
import datetime;

class UpdateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField();
    images = serializers.SerializerMethodField();

    class Meta:
        model = Update;
        fields = ['jobuser', 'date', 'comment', 'username', 'random_string', 'images'];
        
    def get_username(self, update):
        return update.jobuser.user.username;
        
    def get_images(self, update):
        return update.image_set.all().exists();