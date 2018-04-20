from django.contrib.auth.decorators import login_required;
from django.contrib.auth.models import User;
from rest_framework.renderers import JSONRenderer;
from django.utils.decorators import method_decorator;
from django.views.generic import TemplateView;
from django.contrib.auth import authenticate, login, logout;
from ourjobfund.settings import STRIPE_TEST_SECRET_KEY;
from notification.views import sendNotifications;
from annoying.functions import get_object_or_None;
from django.db.models import Q, F;
from django.shortcuts import render, get_object_or_404, redirect;
from update.models import Update;
from .serializers import PledgeHistorySerializer, WorkHistorySerializer;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from user.models import Profile;
from job.models import Job;
from itertools import chain;
from operator import attrgetter
from datetime import datetime;
from .models import JobUser, PledgePay, Pledge, Work, Finish, StripePay, MiscPay;
from .forms import PledgeForm, PayForm, WorkForm, FinishForm;
from random import randint;
import json, stripe;

class PledgeView(TemplateView):
    template_name = 'jobuser/pledge.html';
    form = PledgeForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        return render(request, self.template_name, self.get_context_data(job=job, form=self.form));
        
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        form = self.form(request.POST);
        if (form.is_valid()):
            jobuser = get_object_or_None(JobUser, user=request.user, job=job);
            amount = float(form.cleaned_data['amount']);
            if (jobuser):
                jobuser.pledging = jobuser.pledging + amount;
            else:
                jobuser = JobUser.create(user=request.user, job=job, pledging=amount);
            jobuser.save();
            pledge = Pledge.create(jobuser=jobuser, amount=amount);
            pledge.save();
            comment = form.cleaned_data['comment'];
            if (comment):
                update = Update.create(jobuser=jobuser, comment=comment);
                update.save();
            job.pledging = job.pledging + amount;
            job.save();
            sendNotifications(jobuser);
            return redirect('job:detail', job_random_string=job.random_string);
        else:
            return render(request, self.template_name, self.get_context_data(job=job, form=form));
        
    def get_context_data(self, **kwargs):
        context = super(PledgeView, self).get_context_data(**kwargs);
        context['job'] = kwargs['job'];
        context['form'] = kwargs['form'];
        return context;

class PayView(TemplateView):
    template_name = 'jobuser/pay.html';
    form = PayForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        jobuser = get_object_or_404(JobUser, user=request.user, job=job);
        return render(request, self.template_name, self.get_context_data(jobuser=jobuser, form=self.form(jobuser=jobuser)));
                    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_None(Job, random_string=kwargs['job_random_string']);
        jobuser = get_object_or_None(JobUser, user=request.user, job=job);
        form = self.form(data=request.POST, jobuser=jobuser);
        if (form.is_valid()):
            type = form.cleaned_data['type'];
            pay_to = form.cleaned_data['pay_to'];
            receiver= get_object_or_404(User, pk=int(pay_to));
            if (Work.objects.filter(jobuser__user=receiver, jobuser__job=job)):
                amount = float(form.cleaned_data['amount']);
                if (type == 'Credit/Debit'):
                    self.pay(request, amount=amount, receiver_username=receiver.username);
                    pay = StripePay.create(sender=jobuser, receiver=receiver, amount=amount);
                    pay.save();
                    jobuser.paid = jobuser.paid + amount;
                    jobuser.save();
                    sender.received = sender.received + amount;
                    sender.save();
                    job.paid = job.paid + amount;
                    job.save();
                    if (job.is_finished()):
                        job.is_finished = True;
                        job.save();
                else:
                    pay = MiscPay.create(sender=jobuser, receiver=get_object_or_None(JobUser, user=get_object_or_None(User, username=receiver), job=job), amount=amount);
                    pay.save();
                comment = form.cleaned_data['comment'];
                if (comment):
                    update = Update.create(jobuser=jobuser, comment=comment);
                    update.save();
                return redirect('job:detail', job.random_string);
            else:
                return Http404();
        else:
            return render(request, self.template_name, self.get_context_data(jobuser=jobuser, form=form));
    
    def get_context_data(self, *args, **kwargs):
        context = super(PayView, self).get_context_data(**kwargs);
        context['jobuser'] = kwargs['jobuser'];
        context['form'] = kwargs['form'];
        return context;
    
    def pay(self, request, **kwargs):
        user = get_object_or_None(User, username=kwargs['receiver_username'])
        if (user):
            stripe.api_key = STRIPE_TEST_SECRET_KEY;
            token = request.POST['stripeToken'];
            amount_paying_in_cents = int(kwargs['amount']) * 100;
            charge = stripe.Charge.create(
                amount = amount_paying_in_cents,
                currency = "usd",
                description = "Payment to " + receiver,
                source = token,
                destination = user.stripe_account_id, 
            );

class WorkView(TemplateView):
    template_name = 'jobuser/work.html';
    form = WorkForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        jobuser = get_object_or_None(JobUser, user=request.user, job=job);
        if (Work.objects.filter(jobuser=jobuser).exists()):
            return redirect('job:detail', job_random_string=job.random_string);
        else:
            return render(request, self.template_name, self.get_context_data(job=job, form=self.form(prefix='work')));
        
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        form = self.form(request.POST, prefix='work');
        jobuser = get_object_or_None(JobUser, user=request.user, job=job);
        if (jobuser and jobuser.work_set.all().exists()):
            return redirect('job:detail', job_random_string=job.random_string);
        elif (form.is_valid()):
            if (jobuser):
                jobuser.work_status = 'Working';
            else:
                jobuser = JobUser(user=request.user, job=job, work_status='Working');
            jobuser.save();
            payment_type = form.cleaned_data['payment_type'];
            if (payment_type == 'Credit/Debit' or payment_type == 'Either'):
                self.pay(request);
            work = Work.create(jobuser=jobuser, payment_type=payment_type);
            work.save();
            comment = form.cleaned_data['comment'];
            if (comment):
                update = Update.create(jobuser=jobuser, comment=comment);
                update.save();
            job.working = job.working + 1;
            if (job.isFinished()):
                job.is_finished = True;
            job.save();
            sendNotifications(jobuser);
            return redirect('job:detail', job_random_string=job.random_string);
        else:
            return render(request, self.template_name, self.get_context_data(job=job, form=form));
        
    def get_context_data(self, **kwargs):
        context = super(WorkView, self).get_context_data(**kwargs);
        context['job'] = kwargs['job'];
        context['form'] = kwargs['form'];
        return context;
        
    def pay(self, request):
        stripe.api_key = STRIPE_TEST_SECRET_KEY;
        token = request.POST['stripeToken'];
        amount_paying_in_cents = 100;
        charge = stripe.Charge.create(
            amount = amount_paying_in_cents,
            currency = "usd",
            description = "Payment to OurJobFund",
            source = token,
        );
        
class FinishView(TemplateView):
    template_name = 'jobuser/finish.html';
    form = FinishForm(prefix='finish');
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        jb = get_object_or_None(JobUser, user=request.user, job=job);
        return render(request, self.template_name, self.get_context_data(job=job, form=self.form));
        
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        form = self.form(request.POST);
        if (form.is_valid()):
            jobuser = get_object_or_None(JobUser, user=request.user, job=job);
            jobuser.work_status = 'Finished';
            jobuser.save();
            finish = Finish.create(jobuser=jobuser);
            finish.save();
            comment = form.cleaned_data['comment'];
            if (comment):
                update = Update(jobuser=jobuser, comment=comment);
                update.save();
            job.finished = job.finished + 1;
            job.save();
            if (job.check_is_finished()):
                job.is_finished = True;
                job.save();
            sendNotifications(jobuser);
            return redirect('job:detail', job_random_string=job.random_string);
        else:
            return render(request, self.template_name, self.get_context_data(job=job, form=form));
        
    def get_context_data(self, **kwargs):
        context = super(FinishView, self).get_context_data(**kwargs);
        context['job'] = kwargs['job'];
        context['form'] = kwargs['form'];
        return context;
       
class PledgeHistoryView(TemplateView):
    template_name = 'jobuser/pledge-history.html';
    
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        return render(request, self.template_name, self.get_context_data(job=job));
        
    def get_context_data(self, **kwargs):
        context = super(PledgeHistoryView, self).get_context_data(**kwargs);
        job = kwargs['job'];
        pledges = Pledge.objects.filter(jobuser__job=job);
        misc_payments = MiscPay.objects.filter(jobuser__job=job);
        stripe_payments = StripePay.objects.filter(jobuser__job=job);
        set = sorted(chain(pledges, misc_payments, stripe_payments), key=attrgetter('date'), reverse=True);
        context['job'] = job;
        context['total'] = len(set);
        context['set'] = set[:50];
        return context;
        
class WorkHistoryView(TemplateView):
    template_name = 'jobuser/work-history.html';
    
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        return render(request, self.template_name, self.get_context_data(job=job));
        
    def get_context_data(self, **kwargs):
        context = super(WorkHistoryView, self).get_context_data(**kwargs);
        job = kwargs['job'];
        work = Work.objects.filter(jobuser__job=job);
        finish = Finish.objects.filter(jobuser__job=job);
        misc_payments = MiscPay.objects.filter(jobuser__job=job);
        stripe_payments = StripePay.objects.filter(jobuser__job=job);
        set = sorted(chain(work, finish, misc_payments, stripe_payments), key=attrgetter('date'), reverse=True);
        context['job'] = job;
        context['total'] = len(set);
        context['set'] = set[:50];
        return context;

def sort_pledge_history(request, job_random_string):
    job = get_object_or_404(Job, random_string=job_random_string);
    if (request.is_ajax()):
        data = sort_history(request, job);
        serializer = PledgeHistorySerializer(data, many=True);
        json = JSONRenderer().render(serializer.data);
        return HttpResponse(json, 'application/json');
    else:
        return redirect('pledge-history', job_random_string=job.random_string);        
        
def sort_work_history(request, job_random_string):
    job = get_object_or_404(Job, random_string=job_random_string);
    if (request.is_ajax()):
        data = sort_history(request, job);
        serializer = WorkHistorySerializer(data, many=True);
        json = JSONRenderer().render(serializer.data);
        return HttpResponse(json, 'application/json');
    else:
        return redirect('pledge-history', job_random_string=job.random_string);
        
def sort_history(request, job):
    numSearches = request.GET['num_searches'];
    column = request.GET['column'];
    ascending_or_descending = request.GET['order'];
    pledges = Pledge.objects.filter(jobuser__job=job);
    misc_payments = MiscPay.objects.filter(jobuser__job=job);
    stripe_payments = StripePay.objects.filter(jobuser__job=job);
    if (column == 'username'):
        key = lambda x: x.get_username().lower();
    elif (column == 'date'):
        key = lambda x: x.get_date();
    elif (column == 'type'):
        key = lambda x: x.get_type().lower();
    elif (column == 'amount'):
        key = lambda x: x.get_amount();
    elif (column == 'to'):
        key = lambda x: x.get_to();
    elif (column == 'from'):    
        key = lambda x: x.get_from();
    else:
        key = lambda x: x.get_confirmed();
    data = sorted(
        chain(pledges, misc_payments, stripe_payments),
        key=key,
    );
    if (ascending_or_descending == 'descending'):
        data = data[::-1];
    return data;
   
class PaymentConfirmationView(TemplateView):
    template_name = 'jobuser/confirmation.html';

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        jobuser = get_object_or_None(JobUser, user=request.user, job=job);
        return render(request, self.template_name, self.get_context_data(jobuser=jobuser));


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        jobuser = get_object_or_None(JobUser, user=request.user, job=job);
        payments = MiscPay.objects.filter(receiver=jobuser, verified=None);
        confirm_or_reject = "";
        pk = "";
        for p in payments:
            if (str(p.pk) in request.POST):
                pk = p.pk;
                confirm_or_reject = request.POST[str(p.pk)];
        misc_pay = get_object_or_None(MiscPay, pk=pk);
        if (misc_pay):
            if (confirm_or_reject == 'confirm'):
                misc_pay.verified = True;
                jobuser.received = jobuser.received + misc_pay.amount;
                jobuser.save()
                misc_pay.jobuser.paid = misc_pay.jobuser.paid +  misc_pay.amount;
                misc_pay.jobuser.save();
                job.paid = job.paid + misc_pay.amount;
                job.save();
                if (job.check_is_finished()):
                    job.is_finished = True;
                    job.save();
            else:
                misc_pay.verified = False;
            misc_pay.save();
            return redirect('payment-confirmation', job_random_string=job.random_string);
        else:
            return render(request, self.template_name, self.get_context_data(jobuser=jobuser));

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentConfirmationView, self).get_context_data(**kwargs);
        jobuser = kwargs['jobuser'];
        context = {
            'jobuser' : jobuser,
            'unconfirmed_payments' : MiscPay.objects.filter(receiver=jobuser, verified=None),
        };
        return context;
        
def addDecimalPlacesForMoney(amount):
    nums = str(amount).split('.');
    if (len(nums) == 2):
        if (len(nums[1]) == 1):
            amount = amount + '0';
    else:
        amount = amount + '.00'
    return amount;    

