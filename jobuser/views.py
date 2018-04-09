from django.contrib.auth.decorators import login_required;
from django.contrib.auth.models import User;
from django.utils.decorators import method_decorator;
from django.views.generic import TemplateView;
from django.contrib.auth import authenticate, login, logout;
from ourjobfund.settings import STRIPE_TEST_SECRET_KEY;
from annoying.functions import get_object_or_None;
from django.db.models import Q, F;
from django.shortcuts import render, get_object_or_404, redirect;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from user.models import Profile;
from job.models import Job;
from .models import JobUser, Pledge, Work, Finish;
from datetime import datetime;
from .forms import PledgeForm, PayForm, WorkForm;
from notification.views import sendNotifications;
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
            pledge = Pledge(jobuser=jobuser, amount=amount);
            pledge.save();
            job.pledged = job.pledged + amount;
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
        user = get_object_or_None(User, username=kwargs['username']);
        job = get_object_or_None(Job, random_string=kwargs['job_random_string']);
        if (request.user == user):
            return redirect('user:detail', username=user.username);
        else:
            return render(request, self.template_name, self.get_context_data(user=user, job=job, form=self.form(sender=request.user, receiver=user)));
                    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user = get_object_or_None(User, username=kwargs['username']);
        job = get_object_or_None(Job, random_string=kwargs['job_random_string']);
        form = self.form(request.POST);
        if (form.is_valid()):
            if (request.user != user):
                job = form.cleaned_data['job'];
                amount = form.cleaned_data['amount'];
                type = form.cleaned_data['type'];
                sender_jobuser = get_object_or_None(JobUser, user=request.user, job=job);
                if (jobuser is None):
                    jobuser = JobUser.create(user=request.user, job=job, paid=0);
                receiver_jobuser = JobUser.objects.get(user=user, job=job);
                if (type == 'Other'):
                    pay = Pay.create(sender_jobuser=sender_jobuser, receiver_jobuser=receiver_jobuser, type="Other", amount=float(amount));
                    pay.save();
                else:
                    self.pay(request, job=job, sender_jobuser=sender_jobuser, receiver_jobuser=receiver_jobuser, amount=amount);
                return redirect('pay:confirmation');
            return redirect('home');
        else:
            return render(request, self.template_name, self.get_context_data(user=user, job=job, form=form));
    
    def get_context_data(self, *args, **kwargs):
        context = super(PayView, self).get_context_data(**kwargs);
        context['receiver'] = kwargs['user'];
        context['job'] = kwargs['job'];
        context['form'] = kwargs['form'];
        return context;
    
    def pay(self, request, **kwargs):
        stripe.api_key = STRIPE_TEST_SECRET_KEY;
        token = request.POST['stripeToken'];
        amount_paying_in_cents = int(kwargs['amount']) * 100;
        sender_jobuser = kwargs['sender_jobuser'];
        receiver_jobuser = kwargs['receiver_jobuser'];
        charge = stripe.Charge.create(
            amount = amount_paying_in_cents,
            currency = "usd",
            description = "Payment to " + receiver_jobuser.user.username + " for " + sender_jobuser.job.name,
            source = token,
        );
        amount_paying_in_dollars = float(amount_paying_in_cents) / 100;
        payment = Pay.create(sender_jobuser=sender_jobuser, receiver_jobuser=receiver_jobuser, amount=amount_paying_in_dollars);
        payment.save();
        sender_jobuser.paid = sender_jobuser.paid + amount_paying_in_dollars;
        sender_jobuser.save();
        receiver_jobuser.received = receiver_jobuser.received + amount_paying_in_dollars;
        receiver_jobuser.save();
        receiver_jobuser.job.paid = receiver_jobuser.job.paid + amount_paying_in_dollars;
        receiver_jobuser.job.save();

class WorkView(TemplateView):
    template_name = 'jobuser/work.html';
    form = WorkForm;
    
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
            if (jobuser):
                jobuser.work_status = 'Working';
            else:
                jobuser = JobUser(user=request.user, job=job, work_status='Working');
            jobuser.save();
            payment_type = form.cleaned_data['payment_type'];
            expected_finish_date = form.cleaned_data['expected_finish_date'];
            minimum_amount_requesting = float(form.cleaned_data['minimum_amount_requesting']);
            work = Work.create(jobuser=jobuser, payment_type=payment_type, expected_finish_date=expected_finish_date, minimum_amount_requesting=minimum_amount_requesting);
            work.save();
            job.workers = job.workers + 1;
            job.save();
            sendNotifications(jobuser);
            return redirect('job:detail', job_random_string=job.random_string);
        else:
            return render(request, self.template_name, self.get_context_data(job=job, form=form));
        
    def get_context_data(self, **kwargs):
        context = super(WorkView, self).get_context_data(**kwargs);
        context['job'] = kwargs['job'];
        context['form'] = kwargs['form'];
        context['type'] = 'Work';
        return context;
        
def VerifyPaymentView(request):
    template_name = 'jobuser/verification.html';
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['random_string']);
        user = get_object_or_404(User, username=kwargs['username']);
        return render(request, self.template_name, get_context_data(job=job, user=user));
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['random_string']);
        user = get_object_or_404(User, username=kwargs['username']);
        sender_jobuser = get_object_or_None(JobUser, job=job, user=user);
        receiver_jobuser = get_object_or_None(JobUser, job=job, user=request.user);
        payments = Pay.objects.filter(Q(sender_jobuser=sender_jobuser) & Q(receiver_jobuser=receiver_jobuser) & Q(verified=False));
        for p in payments:
            if ("verify-" + str(p.pk)):
                p.verified = True;
                p.save();
                return redirect("job:detail", job_random_string=job.random_string);
            if ("reject-" + str(p.pk)):
                p.delete();
                return redirect("job:detail", job_random_string=job.random_string);
        return render(request, self.template_name, get_context_data(job=job, user=user));
            
    def get_context_data(self, *args, **kwargs):
        context = {
            'job' : kwargs['job'],
            'user' : kwargs['user'],
        };
        return context;

def payment_confirmation(request, job_random_string):
    job = get_object_or_404(Job, random_string = job_random_string);
    return render(request, 'pay/confirmed.html', {'job' : job});
    
def addDecimalPlacesForMoney(amount):
    nums = str(amount).split('.');
    if (len(nums) == 2):
        if (len(nums[1]) == 1):
            amount = amount + '0';
    else:
        amount = amount + '.00'
    return amount;    

