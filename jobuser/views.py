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
        return render(request, self.template_name, self.get_context_data(jobuser=jobuser, form=self.form(job=job)));
        
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        form = self.form(data=request.POST, job=job);
        if (form.is_valid()):
            amount = form.cleaned_data['amount'];
            sender = get_object_or_None(JobUser, user=request.user, job=job);
            receiver_user = get_object_or_404(User, username=form.cleaned_data['receiver']);
            receiver = get_object_or_None(JobUser, user=receiver_user, job=job);
            if (form.cleaned_data['pay_through'] == 'Stripe'):
                self.pay(request, amount=amount, receiver=receiver);
                pay = StripePay.create(jobuser=sender, receiver=receiver, amount=amount);
            else:
                pay = MiscPay.create(jobuser=sender, receiver=receiver, amount=amount);
            pay.save();
            comment = form.cleaned_data['comment'];
            if (comment):
                update = Update.create(jobuser=jobuser, comment=comment);
                update.save();
            sender.paid = sender.paid + amount;
            sender.save();
            receiver.received = receiver.received + amount;
            receiver.save();
            job.paid = job.paid + amount;
            job.save();
            if (job.is_finished()):
                job.is_finished = True;
                job.save();
            return redirect('user:detail', username=kwargs['username']);
        else:
            return render(request, self.template_name, self.get_context_data(form=form));
        
    def get_context_data(self, *args, **kwargs):
        context = super(PayView, self).get_context_data(**kwargs);
        context['form'] = kwargs['form'];
        return context;

    def pay(self, request, **kwargs):
        user = get_object_or_None(User, username=kwargs['receiver']);
        if (user):
            stripe.api_key = STRIPE_TEST_SECRET_KEY;
            token = request.POST['stripeToken'];
            amount_paying_in_cents = int(kwargs['amount']) * 100;
            charge = stripe.Charge.create(
                amount = amount_paying_in_cents,
                currency = "usd",
                description = "Payment to " + user.get_username(),
                source = token,
                destination = user.profile.stripe_account_id,
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
            return render(request, self.template_name, self.get_context_data(job=job, form=self.form));
        
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        form = self.form(request.POST);
        jobuser = get_object_or_None(JobUser, user=request.user, job=job);
        if (jobuser and jobuser.work_set.all().exists()):
            return redirect('job:detail', job_random_string=job.random_string);
        elif (form.is_valid()):
            if (jobuser):
                jobuser.work_status = 'Working';
            else:
                jobuser = JobUser(user=request.user, job=job, work_status='Working');
            jobuser.save();
            work = Work.create(
                jobuser=jobuser,
            );
            work.save();
            comment = form.cleaned_data['comment'];
            if (comment):
                update = Update.create(jobuser=jobuser, comment=comment);
                update.save();
            job.working = job.working + 1;
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
    form = FinishForm;
    
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
            if (job.set_is_finished()):
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
        pledges = Pledge.objects.filter(jobuser__job=job);
        misc_payments = MiscPay.objects.filter(jobuser__job=job);
        stripe_payments = StripePay.objects.filter(jobuser__job=job);
        data = sort_history(request, job, chain(pledges, misc_payments, stripe_payments));
        serializer = PledgeHistorySerializer(data, many=True);
        json = JSONRenderer().render(serializer.data);
        return HttpResponse(json, 'application/json');
    else:
        return redirect('pledge-history', job_random_string=job.random_string);        
        
def sort_work_history(request, job_random_string):
    job = get_object_or_404(Job, random_string=job_random_string);
    if (request.is_ajax()):
        work = Work.objects.filter(jobuser__job=job);
        finish = Finish.objects.filter(jobuser__job=job);
        misc_payments = MiscPay.objects.filter(jobuser__job=job);
        stripe_payments = StripePay.objects.filter(jobuser__job=job);
        data = sort_history(request, job, chain(work, finish, misc_payments, stripe_payments));
        serializer = WorkHistorySerializer(data, many=True);
        json = JSONRenderer().render(serializer.data);
        return HttpResponse(json, 'application/json');
    else:
        return redirect('pledge-history', job_random_string=job.random_string);
        
def sort_history(request, job, chain):
    numSearches = request.GET['num_searches'];
    column = request.GET['column'];
    ascending_or_descending = request.GET['order'];
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
        chain,
        key=key,
    );
    if (ascending_or_descending == 'descending'):
        data = data[::-1];
    return data;
   
class UnconfirmedPaymentView(TemplateView):
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
        payments = MiscPay.objects.filter(jobuser=jobuser, confirmed=None);
        confirm_or_reject = "";
        pk = "";
        for p in payments:
            if (str(p.pk) in request.POST):
                pk = p.pk;
                confirm_or_reject = request.POST[str(p.pk)];
        misc_pay = get_object_or_None(MiscPay, pk=pk);
        if (misc_pay):
            if (confirm_or_reject == 'confirm'):
                misc_pay.confirmed = True;
                jobuser.received = jobuser.received + misc_pay.amount;
                jobuser.save()
                misc_pay.jobuser.paid = misc_pay.jobuser.paid +  misc_pay.amount;
                misc_pay.jobuser.save();
                job.paid = job.paid + misc_pay.amount;
                job.save();
                if (job.set_is_finished()):
                    job.is_finished = True;
                    job.save();
            else:
                misc_pay.confirmed = False;
            misc_pay.save();
            return redirect('unconfirmed-payments', job_random_string=job.random_string);
        else:
            return render(request, self.template_name, self.get_context_data(jobuser=jobuser));

    def get_context_data(self, *args, **kwargs):
        context = super(UnconfirmedPaymentView, self).get_context_data(**kwargs);
        jobuser = kwargs['jobuser'];
        context = {
            'jobuser' : jobuser,
            'unconfirmed_payments' : MiscPay.objects.filter(jobuser=jobuser, confirmed=None),
        };
        return context;
        
class ModerateView(TemplateView):
    template_name = 'jobuser/moderate.html';
    
    @method_decorator(login_required)    
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        jobuser = get_object_or_None(JobUser, user=request.user, job=job);
        if (jobuser.moderator_set.all().first()):
            return render(request, self.template_name, self.get_context_data(job=job, jobuser=jobuser));
        else:
            return redirect('job:detail', job.random_string);
        
    def get_context_data(self, request):
        context = super(ModerateView, self).get_context_data(**kwargs);
        mods = None;
        mod = kwargs['jobuser'].moderator_set.filter(active=True).order_by('-date').first();
        if (mod.is_super):
            moderators = Moderator.objects.filter(active=True, jobuser=mod.jobuser);
        else:
            moderators = Moderator.objects.filter(active=True, jobuser__job=kwargs['job']);
        users_jobusers = JobUser.objects.filter(job=job);
        for m in moderators:
            users_jobusers = users_jobusers.exclude(jobuser=m.jobuser);
        context['job'] = kwargs['job'];
        context['jobuser'] = kwargs['jobuser'];
        context['updates'] = Update.objects.filter(jobuser__job=kwargs['job']);
        context['users_jobusers'] = users_jobusers;
        
def addDecimalPlacesForMoney(amount):
    nums = str(amount).split('.');
    if (len(nums) == 2):
        if (len(nums[1]) == 1):
            amount = amount + '0';
    else:
        amount = amount + '.00'
    return amount;    

