from django.contrib.auth.decorators import login_required;
from django.utils.decorators import method_decorator;
from django.views.generic import TemplateView;
from notification.views import sendNotifications;
from annoying.functions import get_object_or_None;
from django.shortcuts import render, get_object_or_404, redirect;
from update.models import Update;
from job.models import Job;
from .models import JobUser;
from .forms import PledgeForm, WorkForm;

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
            if (jobuser is None):
                jobuser = JobUser.create(user=request.user, job=job);
            description = form.cleaned_data['description'];
            amount = float(form.cleaned_data['amount']);
            title = "Pledged $" + addDecimalPlacesForMoney(str(amount));
            jobuser.pledged = jobuser.pledged + amount;
            jobuser.save();
            update = Update.create(jobuser=jobuser, title=title, description=description, pledge=amount);
            update.save();
            job.pledged = job.pledged + amount;
            job.save();
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
        jobuser = get_object_or_None(JobUser, user=request.user, job=job);
        form = self.form(request.POST);
        if (form.is_valid()):
            if (jobuser is None):
                jobuser = JobUser(user=request.user, job=job);
            description = form.cleaned_data['description'];
            type = form.cleaned_data['type'];
            title = type;
            jobuser.work_status = type;
            jobuser.save();
            update = Update.create(jobuser=jobuser, title=title, description=description, work_status=type);
            update.save();
            sendNotifications(jobuser);
            return redirect(job);
        else:
            return render(request, self.template_name, self.get_context_data(job=job, form=form));
        
    def get_context_data(self, **kwargs):
        context = super(WorkView, self).get_context_data(**kwargs);
        context['job'] = kwargs['job'];
        context['form'] = kwargs['form'];
        context['type'] = 'Work';
        return context;
    
def addDecimalPlacesForMoney(amount):
    nums = str(amount).split('.');
    if (len(nums) == 2):
        if (len(nums[1]) == 1):
            amount = amount + '0';
    else:
        amount = amount + '.00'
    return amount;