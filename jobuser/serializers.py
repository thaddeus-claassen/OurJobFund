from rest_framework import serializers;
from .models import JobUser;
from ourjobfund.settings import REST_FRAMEWORK;

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
    date = serializers.SerializerMethodField();

    class Meta:
        model = JobUser;
        fields = ['pledging', 'paid', 'username', 'date'];
        
    def get_username(self, jobuser):
        return jobuser.user.username;
        
    def get_date(self, jobuser):
        return jobuser.pledge_set.all().first().date.strftime(format=REST_FRAMEWORK['DATETIME_FORMAT']);
        
class WorkSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField();
    date = serializers.SerializerMethodField();

    class Meta:
        model = JobUser;
        fields = ['work_status', 'received', 'username', 'date'];
        
    def get_username(self, jobuser):
        return jobuser.user.username;
        
    def get_date(self, jobuser):
        return jobuser.pledge_set.all().first().date.strftime(format=REST_FRAMEWORK['DATETIME_FORMAT']);