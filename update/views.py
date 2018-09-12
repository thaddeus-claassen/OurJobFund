from django.contrib.auth.decorators import login_required;
from django.contrib.auth.models import User;
from django.utils.decorators import method_decorator;
from django.views.generic import TemplateView;
from notification.views import sendNotifications;
from annoying.functions import get_object_or_None;
from django.shortcuts import render, get_object_or_404, redirect;
from jobuser.models import JobUser;
from django.http import HttpResponse, Http404;
from user.models import Profile;
from job.models import Job;
from .models import Update, Image;
from .forms import UpdateForm;
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
            comment = form.cleaned_data['comment'];
            if (comment != "" or len(request.FILES) > 0):
                jobuser = JobUser.objects.get(user=request.user, job=job);
                update = Update.create(jobuser=jobuser, comment=comment);
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
    
def images(request, update_random_string):
    update = get_object_or_404(Update, random_string=update_random_string);
    context = {
        'update' : update,
    }
    return render(request, 'update/images.html', context);
    
class DeleteUpdateView(TemplateView):
    template_name = 'update/delete.html';
        
    def get(self, request, *args, **kwargs):
        update = get_object_or_404(Update, random_string=kwargs['update_random_string']);
        jobuser = get_object_or_None(JobUser, user=request.user, job=update.jobuser.job);
        moderator = jobuser.moderator_set.filter(active=True).order_by('-date').first();
        if (moderator is not None):
            if (update.jobuser.moderator_set.filter(active=True).order_by('-date').first() is not None or moderator.is_super):
                return render(request, self.template_name, self.get_context_data(update=update));
        return redirect('job:detail', job_random_string=update.jobuser.job);
        
    def post(self, request, *args, **kwargs):
        update = get_object_or_404(Update, random_string=kwargs['update_random_string']);
        jobuser = get_object_or_None(JobUser, user=request.user, job=update.jobuser.job);
        moderator = jobuser.moderator_set.filter(active=True).order_by('-date').first();
        if (moderator is not None):
            if (update.jobuser.moderator_set.filter(active=True).order_by('-date').first() is not None or moderator.is_super):
                if ('Delete' in request.POST):
                    update.banned = True;
                    update.save();
                    return redirect('job:moderate', job_random_string=jobuser.job.random_string);
        return redirect('job:detail', random_string=update.random_string);
        
    def get_context_data(self, *args, **kwargs):
        context = super(DeleteUpdateView, self).get_context_data(**kwargs);
        context['update'] = kwargs['update'];
        return context;
    