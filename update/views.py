from django.contrib.auth.decorators import login_required;
from django.contrib.auth.models import User;
from django.utils.decorators import method_decorator;
from django.views.generic import TemplateView;
from ourjobfund.settings import STRIPE_TEST_SECRET_KEY;
from notification.views import sendNotifications;
from annoying.functions import get_object_or_None;
from django.shortcuts import render, get_object_or_404, redirect;
from jobuser.models import JobUser;
from django.http import HttpResponse, Http404;
from user.models import Profile;
from job.models import Job;
from pay.models import Pay;
from .models import Update, Image;
from .forms import UpdateForm, PayForm;
import stripe;

class CreateUpdateView(TemplateView):
    template_name = 'update/create.html';
    form = UpdateForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_None(Job, random_string=kwargs['job_random_string']);
        return render(request, self.template_name, self.get_context_data(job=job, form=self.form));
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        form = self.form(request.POST);
        if (form.is_valid()):
            description = form.cleaned_data['description'];
            if (description != "" or len(request.FILES) > 0):
                jobuser = JobUser.objects.get(user=request.user, job=job);
                update = Update.create(jobuser=jobuser, description=description);
                update.save();
                for image in request.FILES.getlist('images'):
                    image = Image(update=update, image=image);
                    image.save();
                sendNotifications(jobuser);
            return redirect('job:detail', job_random_string=job.random_string);
        else:
            return render(request, self.template_name, self.get_context_data(job=job, form=form));
    
    def get_context_data(self, **kwargs):
        context = super(CreateUpdateView, self).get_context_data(**kwargs);
        context['job'] = kwargs['job'];
        context['form'] = kwargs['form'];
        return context;
    
class PayView(TemplateView):
    template_name = 'update/create.html';
    form = PayForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        profile = get_object_or_None(Profile, random_string=kwargs['profile_random_string']);
        job = get_object_or_None(Job, random_string=kwargs['job_random_string']); 
        if (profile is not None and job is not None):
            user = User.objects.get(profile=profile);
            if (request.user != user):
                receiver_jobuser = get_object_or_None(JobUser, user=user, job=job);
                if (receiver_jobuser and receiver_jobuser.work_status != ''):
                    return render(request, self.template_name, self.get_context_data(job=job, receiver_jobuser=receiver_jobuser, form=self.form));
        return redirect('home');
                    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        profile = get_object_or_None(Profile, random_string=kwargs['profile_random_string']);
        job = get_object_or_None(Job, random_string=kwargs['job_random_string']); 
        form = self.form(request.POST);
        if (form.is_valid()):
            user = User.objects.get(profile=profile);
            if (request.user != user):
                receiver_jobuser = get_object_or_None(JobUser, user=user, job=job);
                if (receiver_jobuser and receiver_jobuser.work_status != ''):
                    sender_jobuser = get_object_or_None(JobUser, user=request.user, job=job);
                    if (sender_jobuser is None):
                        sender_jobuser = JobUser(user=request.user, job=job);
                        sender_jobuser.save();
                    amount = form.cleaned_data['amount'];
                    title = "Paid $" + addDecimalPlacesForMoney(amount);
                    update = Update.create(jobuser=sender_jobuser, title=title, description=form.cleaned_data['description'], paid=amount);
                    update.save();
                    type = form.cleaned_data['type'];
                    if (type == 'Other'):
                        pay = Pay.create(sender_jobuser=sender_jobuser, receiver_jobuser=receiver_jobuser, type="Other", amount=float(amount));
                        pay.save();
                    else:
                        self.pay(request, job=job, sender_jobuser=sender_jobuser, receiver_jobuser=receiver_jobuser, amount=amount);
                        return redirect('pay:confirmation', job.random_string);
                    return redirect(job);
            return redirect('home');
        else:
            return render(request, self.template_name, self.get_context_data(job=job, receiver_jobuser=receiver_jobuser, form=form));
    
    def get_context_data(self, **kwargs):
        context = super(PayView, self).get_context_data(**kwargs);
        context['job'] = kwargs['job'];
        context['receiver_jobuser'] = kwargs['receiver_jobuser'];
        context['form'] = kwargs['form'];
        return context; 
    
    def pay(self, request, **kwargs):
        stripe.api_key = STRIPE_TEST_SECRET_KEY;
        token = request.POST['stripeToken'];
        amount_paying_in_cents = int(kwargs['amount']) * 100;
        charge = stripe.Charge.create(
            amount = amount_paying_in_cents,
            currency = "usd",
            description = sender_jobuser.user.username + " paying " + receiver_jobuser.user.username + " for " + sender_jobuser.job.name,
            source = token,
        );
        amount_paying_in_dollars = float(amount_paying_in_cents) / 100;
        sender_jobuser = kwargs['sender_jobuser'];
        receiver_jobuser = kwargs['receiver_jobuser'];
        payment = Pay.create(sender_jobuser=sender_jobuser, receiver_jobuser=receiver_jobuser, amount=amount_paying_in_dollars);
        payment.save();
        sender_jobuser.paid = sender_jobuser.paid + amount_paying_in_dollars;
        sender_jobuser.save();
        receiver_jobuser.received = receiver_jobuser.received + amount_paying_in_dollars;
        receiver_jobuser.save();
        receiver_jobuser.job.paid = receiver_jobuser.job.paid + amount_paying_in_dollars;
        receiver_jobuser.job.save();
    
def detail(request, update_random_string):
    update = get_object_or_404(Update, random_string=update_random_string);
    context = {
        'update' : update,
    }
    return render(request, 'update/detail.html', context);
    
def addDecimalPlacesForMoney(amount):
    nums = float(amount).split('.');
    if (len(nums) == 2):
        if (len(num[1]) == 1):
            amount = amount + '0';
    else:
        amount = amount + '.00'
    return amount;