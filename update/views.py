from django.contrib.auth.decorators import login_required;
from django.shortcuts import render, get_object_or_404, redirect;
from django.utils.decorators import method_decorator;
from django.http import HttpResponse, Http404;
from django.contrib.auth.models import User;
from jobuser.models import JobUser;
from .models import Update, Image;
from pledge.models import Pledge, Pay;
from work.models import Work;
from notification.views import sendNotifications;
from django.views.generic import TemplateView;
from job.models import Job;
from .forms import UpdateForm;
from random import randint;
from annoying.functions import get_object_or_None;
import stripe;
    
class CreateView(TemplateView):
    template_name = 'update/create.html';
    form = UpdateForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_None(Job, random_string=kwargs['job_random_string']);
        return render(request, self.template_name, self.get_context_data(job=job, form=self.form(user=request.user, job=job)));
    
    @method_decorator(login_required)    
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        form = self.form(request.POST);
        print(form)
        if (form.is_valid()):
            jobuser = get_object_or_None(JobUser, user=request.user, job=job);
            if (jobuser is None):
                jobuser = JobUser(user=request.user, job=job);
                jobuser.save();
            description = form.cleaned_data['description'];
            title = form.cleaned_data['title'];
            type = form.cleaned_data['type'];
            if (type == 'Comment'):
                for image in request.FILES.getlist('images'):
                    image = Image(image=image, update=update);
                    image.save();
            elif (type == 'Pledge'):
                amount = form.cleaned_data['amount'];
                user = request.user;
                job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
                pledge = Pledge(jobuser=jobuser, amount=amount, comment=description, random_string=createRandomString());
                pledge.save();
                jobuser.amount_pledged = jobuser.amount_pledged + amount;
                jobuser.save();
                job.pledged = job.pledged + amount;
                job.save();
                title = "Pledged $" + str(amount);
            elif (type == 'Working' or type == 'Finished'):
                work = Work(jobuser=jobuser, status=type, comment=description);
                work.save();
                if (type == 'Working'):
                    job.workers = job.workers + 1;
                    title = "Started Working";
                else:
                    job.finished = job.finished + 1;
                    title = "Finished Working";
            elif (type == 'Pay'):
                self.pay(request, job, jobuser);
            update = Update(jobuser=jobuser, title=title, description=description, random_string=createRandomString());
            update.save();
            sendNotifications(jobuser);
            return redirect(job);
        else:
            return render(request, self.template_name, self.get_context_data(jobuser=jobuser, form=form));
            
    def pay(self, request, job, jobuser):
        receiver_pk = request.POST['pay_to'];
        stripe.api_key = STRIPE_TEST_SECRET_KEY;
        token = request.POST['stripeToken'];
        amount_paying_in_cents = int(request.POST['pay_amount']);
        charge = stripe.Charge.create(
            amount = amount_paying_in_cents,
            currency = "usd",
            description = "Does this charge work?",
            source = token,
        );
        amount_paying_in_dollars = float(amount_paying_in_cents) / 100;
        payment = Pay(jobuser=jobuser, receiver=jobuser.user, amount=amount_paying_in_dollars);
        payment.save();
        jobuser.amount_paid = jobuser.amount_paid + amount_paying_in_dollars;
        jobuser.save();
        receiver_jobuser = JobUser.objects.get(user=User.objects.get(id=receiver_pk), job=job);
        receiver_jobuser.amount_received = receiver_jobuser.amount_received + amount_paying_in_dollars;
        receiver_jobuser.save();
        job.paid = job.paid + amount_paying_in_dollars;
        job.save();
    
    def get_context_data(self, **kwargs):
        context = {
            'job' : kwargs['job'],
            'form' : kwargs['form'],
        }
        return context;
    
def detail(request, update_random_string):
    update = get_object_or_404(Update, random_string=update_random_string);
    context = {
        'update' : update,
    }
    return render(request, 'update/detail.html', context);
    
def createRandomString():
    random_string = '';
    available_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
    for i in range(50):
        index = randint(0, 61);
        random_char = available_chars[index];
        random_string = random_string + random_char;
    if (Update.objects.filter(random_string=random_string).exists()):
        random_string = createRandomString();
    return random_string;
    
    
    
    
    
    
    
    
    
    
