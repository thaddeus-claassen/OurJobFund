from rest_framework import serializers;
from .models import Update;

class UpdateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField();
    date = serializers.DateTimeField(format="%d/%m/%y")

    class Meta:
        model = Update;
        fields = ['jobuser', 'date', 'description', 'username'];
        
    def get_username(self, update):
        return update.jobuser.user.username;