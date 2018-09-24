from rest_framework import serializers;
from .models import JobUser;
from ourjobfund.settings import REST_FRAMEWORK;
from datetime import datetime;

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
    started = serializers.SerializerMethodField();
    finished = serializers.SerializerMethodField();

    class Meta:
        model = JobUser;
        fields = ['received', 'username', 'started', 'finished'];
        
    def get_username(self, jobuser):
        return jobuser.user.username;
        
    def get_started(self, jobuser):
        return jobuser.work_set.all().first().date.strftime(format=REST_FRAMEWORK['DATETIME_FORMAT']);
        
    def get_finished(self, jobuser):
        finished = None;
        if (jobuser.finish_set.all().exists()):
            finished = jobuser.finish_set.all().first().date.strftime(format=REST_FRAMEWORK['DATETIME_FORMAT']);
        else:
            finished = datetime(3000, 1, 1).strftime(format=REST_FRAMEWORK['DATETIME_FORMAT']);
        return finished;
        
class PledgeHistorySerializer(serializers.Serializer):
    username = serializers.SerializerMethodField();
    date = serializers.SerializerMethodField();
    type = serializers.SerializerMethodField();
    amount = serializers.SerializerMethodField();
    to = serializers.SerializerMethodField();
    confirmed = serializers.SerializerMethodField();
    
    def get_username(self, pledge_pay):
        return pledge_pay.get_username();
        
    def get_date(self, pledge_pay):
        return pledge_pay.get_date().strftime(format=REST_FRAMEWORK['DATETIME_FORMAT']);
        
    def get_type(self, pledge_pay):
        return pledge_pay.get_type();
       
    def get_amount(self, pledge_pay):
        return pledge_pay.get_amount();
        
    def get_to(self, pledge_pay):
        return pledge_pay.get_to();
        
    def get_confirmed(self, pledge_pay):
        return pledge_pay.get_confirmed();
        
class WorkHistorySerializer(serializers.Serializer):
    username = serializers.SerializerMethodField();
    date = serializers.SerializerMethodField();
    type = serializers.SerializerMethodField();
    amount = serializers.SerializerMethodField();
    sender = serializers.SerializerMethodField();
    confirmed = serializers.SerializerMethodField();
    
    def get_username(self, work_finish):
        return work_finish.get_to();
        
    def get_date(self, work_finish):
        return work_finish.get_date().strftime(format=REST_FRAMEWORK['DATETIME_FORMAT']);
        
    def get_type(self, work_finish):
        return work_finish.get_type();
       
    def get_amount(self, work_finish):
        return work_finish.get_amount();
        
    def get_sender(self, work_finish):
        return work_finish.get_from();
        
    def get_confirmed(self, work_finish):
        return work_finish.get_confirmed();
       