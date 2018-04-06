from rest_framework import serializers;
from .models import JobUser;

class JobUserSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField();
    random_string = serializers.SerializerMethodField();
    
    class Meta:
        model = JobUser;
        fields = ['pledging', 'paid', 'work_status', 'received', 'title', 'random_string'];

    def get_title(self, jobuser):
        return jobuser.job.title;
        
    def get_random_string(self, jobuser):
        return jobuser.job.random_string;
        
class PledgeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField();

    class Meta:
        model = JobUser;
        fields = ['pledging', 'paid', 'username'];
        
    def get_username(self, jobuser):
        return jobuser.user.username;
        
class WorkSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField();

    class Meta:
        model = JobUser;
        fields = ['work_status', 'received', 'username'];
        
    def get_username(self, jobuser):
        return jobuser.user.username;