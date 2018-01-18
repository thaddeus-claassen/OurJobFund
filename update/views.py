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
    
class CreateView(TemplateView):
    template_name = 'update/create.html';
    form = UpdateForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_None(Job, random_string=kwargs['job_random_string']);
        jobuser = get_object_or_None(JobUser, user=user, job=job);
        if (jobuser):
            jobuser.amount_pledged = jobuser.amount_pledged + amount;
        else:
            jobuser = JobUser(user=user, job=job, amount_pledged=amount);
        jobuser.save();
        return render(request, self.template_name, self.get_context_data(jobuser=jobuser, form=self.form));
    
    @method_decorator(login_required)    
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        jobuser = get_object_or_404(JobUser, user=request.user, job=job);
        form = self.form(request.POST);
        if (form.is_valid()):
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
            update = Update(jobuser=jobuser, title=title, description=description, random_string=createRandomString());
            update.save();
            sendNotifications(jobuser);
            return redirect(job);
        else:
            return render(request, self.template_name, self.get_context_data(jobuser=jobuser, form=form));
    
    def get_context_data(self, **kwargs):
        context = {
            'jobuser' : kwargs['jobuser'],
            'form' : kwargs['form'],
        }
        return context;
    
    
def create_update_by_paying(payment):
    update = Update(jobuser=payment.jobuser, title="Paid " + str(payment.receiver.username) + " $" + str(payment.amount / 100) + ".00", random_string=createRandomString());
    update.save();
    sendNotifications(update);

def create_update_by_finishing(finish):
    update = Update(jobuser=finish.jobuser, title="Finished");
    update.save();
    sendNotifications(update);
    
def create_update_by_unfinishing(unfinish):
    update = Update(jobuser=unfinish.jobuser, title="Unfinished");
    update.save();
    sendNotifications(update);
    
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
    
    
    
    
    
    
    
    
    
    
