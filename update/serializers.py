from rest_framework import serializers;
from .models import Update;
import datetime;

class UpdateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField();

    class Meta:
        model = Update;
        fields = ['jobuser', 'date', 'comment', 'username'];
        
    def get_username(self, update):
        return update.jobuser.user.username;
        
            