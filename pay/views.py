from django.contrib.auth.decorators import login_required;
from django.contrib.auth.models import User;
from django.utils.decorators import method_decorator;
from django.views.generic import TemplateView;
from django.contrib.auth import authenticate, login, logout;
from ourjobfund.settings import STRIPE_TEST_SECRET_KEY, STATIC_ROOT;
from ourjobfund.settings import STRIPE_TEST_SECRET_KEY;
from annoying.functions import get_object_or_None;
from django.db.models import Q, F;
from django.shortcuts import render, get_object_or_404, redirect;
from django.forms import formset_factory;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from user.models import Profile;
from job.models import Job;
from datetime import datetime;
from .models import Pay;
from .forms import PayForm;
from random import randint;
import json, stripe;

class PayView(TemplateView):
    template_name = 'pay/pay.html';
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
                sender_jobuser = JobUser.objects.get(user=request.user, job=job);
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
    

def payment_confirmation(request, job_random_string):
    job = get_object_or_404(Job, random_string = job_random_string);
    return render(request, 'pay/confirmed.html', {'job' : job});