from django.contrib.auth.decorators import login_required;
from django.contrib.auth.models import User;
from django.utils.decorators import method_decorator;
from django.views.generic import TemplateView;
from notification.views import sendNotifications;
from annoying.functions import get_object_or_None;
from django.shortcuts import render, get_object_or_404, redirect;
from jobuser.models import JobUser;
from django.http import HttpResponse, Http404;
from job.models import Job;
from pay.models import Pay;
from .models import Update, Image;
from .forms import UpdateForm;
from random import randint;
import stripe;
    
class CreateView(TemplateView):
    template_name = 'update/create.html';
    form = UpdateForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_None(Job, random_string=kwargs['job_random_string']);
        type = "";
        if ('update' in request.GET):
            type = 'update';
        elif ('pledge' in request.GET):
            type = 'pledge';
        elif ('work' in request.GET):
            type = 'work';
        else:
            return redirect(job);
        return render(request, self.template_name, self.get_context_data(type=type, job=job, form=self.form));
    
    @method_decorator(login_required)    
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        form = self.form(request.POST);
        if (form.is_valid()):
            jobuser = get_object_or_None(JobUser, user=request.user, job=job);
            if (jobuser is None):
                jobuser = JobUser(user=request.user, job=job);
                jobuser.save();
            description = form.cleaned_data['description'];
            update = Update(jobuser=jobuser, description=description);
            if ('update' in request.POST):
                for image in request.FILES.getlist('images'):
                    image = Image(update=update, image=image);
                    image.save();
                title = "Update";
            elif ('pledge' in request.POST):
                amount = form.cleaned_data['amount'];
                jobuser.pledged = jobuser.pledged + amount;
                jobuser.save();
                job.pledged = job.pledged + amount;
                job.save();
                title = "Pledged $" + str(amount);
            elif ('work' in request.POST):
                jobuser.request = form.cleaned_data['money_request'];
                if (jobuser.work_status == 'work'):
                    jobuser.work_status = 'work';
                    title = "Started Working";
                else:
                    jobuser.work_static = 'finish';
                    title = "Finished Working";
                jobuser.save();
            update.title = title;
            update.save();
            sendNotifications(jobuser);
            return redirect(job);
        else:
            type = "";
            if ('update' in request.POST):
                type = 'update';
            elif ('pledge' in request.POST):
                type = 'pledge';
            elif ('work' in request.POST):
                type = 'work';
            return render(request, self.template_name, self.get_context_data(type=type, job=job, form=form));
    
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs);
        context = {
            'type' : kwargs['type'],
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
