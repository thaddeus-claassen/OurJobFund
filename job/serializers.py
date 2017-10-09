from rest_framework import serializers;
from .models import Job;
from jobuser.models import JobUser, Pledge, Work, Pay;
import datetime;
from django.db.models import Count, Q

class JobSerializer(serializers.ModelSerializer):
    expected_pay = serializers.SerializerMethodField();
    expected_workers = serializers.SerializerMethodField();

    class Meta:
        model = Job;
        fields = ['name', 'creation_date', 'pledged', 'paid', 'workers', 'finished', 'expected_pay', 'expected_workers'];
            
    def get_expected_pay(self, job):
        pledges = Pledge.objects.filter(jobuser__job=job);
        pledges = self.notBeenActiveInTheLastNDays(pledges, self.context['user'].pledgefilter.not_been_active_in_the_last_n_days);
        pledges = self.paidAtLeastNTimes(pledges, self.context['user'].pledgefilter.paid_at_least_n_times);
        pledges = self.paidAtLeastNAmountInTotal(pledges, self.context['user'].pledgefilter.paid_at_least_n_amount_in_total);
        return self.calculateExpectedPledged(pledges);
    
    def notBeenActiveInTheLastNDays(self, queryset, n):
        return queryset.exclude(jobuser__user__last_login__lte=(datetime.datetime.now() - datetime.timedelta(days=n)));
        
    def paidAtLeastNTimes(self, pledges, n):
        for pledge in pledges:
            num_times_paid = JobUser.objects.filter(Q(user=self.context['user']) & Q(pay__isnull=False)).count();
            if (num_times_paid < n):
                pledges = pledges.exclude(pk=pledge.pk);
        return pledges;
        
    def paidAtLeastNAmountInTotal(self, pledges, n):
        for pledge in pledges:
            user = pledge.jobuser.user;
            total = 0;
            for payment in Pay.objects.filter(jobuser__user=user):
                total = total + payment.amount;
            if (total < n):
                pledges = pledges.exclude(pk=pledge.pk);
        return pledges;
       
    def calculateExpectedPledged(self, pledges):
        expected_pledged = 0;
        for pledge in pledges:
            expected_pledged = expected_pledged + pledge.amount;
        return expected_pledged;    
        
    def get_expected_workers(self, job):
        workers = Work.objects.filter(jobuser__job=job);
        workers = self.notBeenActiveInTheLastNDays(workers, self.context['user'].workerfilter.not_been_active_in_the_last_n_days);
        return workers.count();
        