from django.contrib.auth.decorators import login_required;
from django.shortcuts import render, get_object_or_404, redirect;
from annoying.functions import get_object_or_None;
from django.utils.decorators import method_decorator;
from django.views.generic import TemplateView;
from notification.views import sendNotifications;
from job.models import Job;
from update.models import Update;
from .forms import PledgeForm, WorkForm;
from .models import JobUser;
from random import randint;

class PledgeView(TemplateView):
    template_name = 'jobuser/create.html';
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
            if (jobuser is None):
                jobuser = JobUser(user=request.user, job=job);
            description = form.cleaned_data['description'];
            amount = float(form.cleaned_data['amount']);
            update = Update(jobuser=jobuser, description=description, pledge=amount, random_string=createRandomString());
            jobuser.pledged = jobuser.pledged + amount;
            jobuser.save();
            job.pledged = job.pledged + amount;
            job.save();
            title = "Pledged $" + str(amount);
            update.title = title;
            update.save();
            sendNotifications(jobuser);
            return redirect(job);
        else:
            return render(request, self.template_name, self.get_context_data(job=job, form=form));
        
    def get_context_data(self, **kwargs):
        context = super(PledgeView, self).get_context_data(**kwargs);
        context['job'] = kwargs['job'];
        context['form'] = kwargs['form'];
        return context;
        
class WorkView(TemplateView):
    template_name = 'jobuser/create.html';
    form = WorkForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        jb = get_object_or_None(JobUser, user=request.user, job=job);
        if (jb and jb.work_status == 'work'):
            type = 'finish';
        else:
            type = 'work';
        return render(request, self.template_name, self.get_context_data(job=job, form=self.form, type=type));
        
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        jobuser = get_object_or_None(JobUser, user=request.user, job=job);
        form = self.form(request.POST);
        if (form.is_valid()):
            if (jobuser is None):
                jobuser = JobUser(user=request.user, job=job);
            description = form.cleaned_data['description'];
            type = form.cleaned_data['type'];
            request_money = float(form.cleaned_data['amount']);
            update = Update(jobuser=jobuser, description=description, request_money=request_money, work_status=type, random_string=createRandomString());
            jobuser.work_status = type;
            if (type == 'work'):
                title = "Started Working";
                jobuser.request_money = request_money;
            else:
                title = "Finished Working";
            jobuser.save();
            update.title = title;
            update.save();
            sendNotifications(jobuser);
            return redirect(job);
        else:
            if (jobuser and jobuser.work_status == 'work'):
                type = 'finished';
            else:
                type = 'working';
            return render(request, self.template_name, self.get_context_data(job=job, form=form, type=type));
        
    def get_context_data(self, **kwargs):
        context = super(WorkView, self).get_context_data(**kwargs);
        context['job'] = kwargs['job'];
        context['form'] = kwargs['form'];
        context['type'] = kwargs['type'];
        return context;
        
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