from rest_framework import serializers;
from .models import Job;
from jobuser.models import JobUser;
from pay.models import Pay;
import datetime;
from django.db.models import Count, Q;
from django.utils import timezone;

class JobSerializer(serializers.ModelSerializer):
    #expected_pay = serializers.SerializerMethodField();
    #expected_workers = serializers.SerializerMethodField();

    class Meta:
        model = Job;
        fields = ['title', 'date', 'pledged', 'paid', 'workers', 'finished', 'random_string', 'latitude', 'longitude'];
        
    ''''
    def get_expected_pay(self, job):
        pledges = JobUser.objects.filter(Q(job=job) & Q(pledged__gt=0));
        if (self.context['user'].is_authenticated()):
            pledges = self.notBeenActiveInTheLastNDays(pledges, self.context['user'].pledgefilter.not_been_active_in_the_last_n_days);
            pledges = self.paidAtLeastNTimes(pledges, self.context['user'].pledgefilter.paid_at_least_n_times);
            pledges = self.paidAtLeastNAmountInTotal(pledges, self.context['user'].pledgefilter.paid_at_least_n_amount_in_total);
        return self.calculateExpectedPledged(pledges);
    
    def notBeenActiveInTheLastNDays(self, queryset, n):
        return queryset.exclude(user__last_login__lte=(timezone.now() - datetime.timedelta(days=n)));
        
    def paidAtLeastNTimes(self, pledges, n):
        for pledge in pledges:
            num_times_paid = JobUser.objects.filter(Q(user=self.context['user']) & Q(paid__gt=0)).count();
            if (num_times_paid < n):
                pledges = pledges.exclude(pk=pledge.pk);
        return pledges;
        
    def paidAtLeastNAmountInTotal(self, pledges, n):
        for pledge in pledges:
            user = pledge.user;
            total = 0;
            for payment in JobUser.objects.filter(Q(user=user) & Q(paid__gt=0)):
                total = total + payment.amount;
            if (total < n):
                pledges = pledges.exclude(pk=pledge.pk);
        return pledges;
       
    def calculateExpectedPledged(self, pledges):
        expected_pledged = 0;
        for pledge in pledges:
            expected_pledged = expected_pledged + pledge.pledged;
        return expected_pledged;    
        
    def get_expected_workers(self, job):
        return job.workers;
        workers = JobUser.objects.filter(Q(job=job) & (Q(work_status='working') | Q(work_status='finished')));
        if (self.context['user'].is_authenticated()):
            workers = self.notBeenActiveInTheLastNDays(workers, self.context['user'].workerfilter.not_been_active_in_the_last_n_days);
        return workers.count();
    '''    