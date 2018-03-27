from rest_framework import serializers;
from ourjobfund.settings import DEBUG;
from .models import Update;

class UpdateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField();

    class Meta:
        model = Update;
        fields = ['jobuser', 'date', 'description', 'username'];
        
    def get_username(self, update):
        return update.jobuser.user.username;
        
            