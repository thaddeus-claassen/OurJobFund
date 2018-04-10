from django.contrib.auth.decorators import login_required;
from django.contrib.auth.models import User;
from django.utils.decorators import method_decorator;
from django.views.generic import TemplateView;
from django.contrib.auth import authenticate, login, logout;
from ourjobfund.settings import STRIPE_TEST_SECRET_KEY;
from notification.views import sendNotifications;
from annoying.functions import get_object_or_None;
from django.db.models import Q, F;
from django.shortcuts import render, get_object_or_404, redirect;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from user.models import Profile;
from job.models import Job;
from update.models import Update;
from .models import JobUser, Pledge, Work, Finish;
from datetime import datetime;
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
            update = Update.create(jobuser=jobuser, comment=comment);
            update.save();
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
    template_name = 'jobuser/work-finish.html';
    form = WorkForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        jb = get_object_or_None(JobUser, user=request.user, job=job);
        if (jb.work_set.all().exists()):
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
            print(jobuser);
            work = Work.create(jobuser=jobuser, payment_type=payment_type);
            work.save();
            comment = form.cleaned_data['comment'];
            update = Update.create(jobuser=jobuser, comment=comment);
            update.save();
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
        return context;
        
class FinishView(TemplateView):
    template_name = 'jobuser/work-finish.html';
    form = FinishForm(prefix='finish');
    
    @method_decorator
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        jb = get_object_or_None(JobUser, user=request.user, job=job); 
        return render(request, self.template_name, self.get_context_data(job=job, form=self.form));
        
    @method_decorator
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        form = self.form(request.POST);
        if (form.is_valid()):
            jobuser = get_object_or_None(JobUser, user=request.user, job=job);
            jobuser.work_status = 'Finished';
            jobuser.save();
            work = Finish.create(jobuser=jobuser);
            work.save();
            job.finished = job.finished + 1;
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
        
class PaymentConfirmationView(TemplateView):
    template_name = 'jobuser/confirmation.html';

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['random_string']);
        jobuser = get_object_or_None(JobUser, user=request.user, job=job);
        if (jobuser.miscpay_set.all().exists()):
            return render(request, self.template_name, get_context_data(jobuser=jobuser));
        else:
            return redirect('job:detail', job_random_string=job.random_string);
        

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['random_string']);
        jobuser = get_object_or_None(JobUser, user=request.user, job=job);
        confirm_or_reject = "";
        pk = "";
        misc_pay = get_object_or_None(MiscPay, pk=pk, jobuser=jobuser);
        if (misc_pay):
            if (confirm_or_reject == 'confirm'):
                misc_pay.verified = True;
            else:
                misc_pay.verified = False;
            misc_pay.save();
            if (jobuser.miscpay_set.all().exists()):
                return redirect('payment-confirmation', job_random_string=job.random_string);
            else:
                return redirect('job:detail', job_random_string=job.random_string);
        else:
            return render(request, self.template_name, get_context_data(job=job, user=user));

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentConfirmationView, self).get_context_data(**kwargs);
        jobuser = kwargs['jobuser'];
        context = {
            'jobuser' : jobuser,
            'unconfirmed_payments' : jobuser.miscpay_set.filter(verified=False),
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

