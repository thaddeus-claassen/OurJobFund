from rest_framework import serializers;
from .models import JobUser;

class JobUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField();
    random_string = serializers.SerializerMethodField();
    
    class Meta:
        model = JobUser;
        fields = ['pledged', 'paid', 'work_status', 'received', 'name', 'random_string'];

    def get_name(self, jobuser):
        return jobuser.job.name;
        
    def get_random_string(self, jobuser):
        return jobuser.job.random_string;
        
class PledgeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField();

    class Meta:
        model = JobUser;
        fields = ['pledged', 'paid', 'username'];
        
    def get_username(self, jobuser):
        return jobuser.user.username;
        
class WorkSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField();

    class Meta:
        model = JobUser;
        fields = ['work_status', 'received', 'username'];
        
    def get_username(self, jobuser):
        return jobuser.user.username;