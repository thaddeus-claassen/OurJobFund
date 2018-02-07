from django.contrib.auth.decorators import login_required;
from django.shortcuts import render, get_object_or_404, redirect;
from annoying.functions import get_object_or_None;
from django.utils.decorators import method_decorator;
from django.views.generic import TemplateView;
from job.models import Job;
from .forms import PledgeForm;
from .models import Pledge;
from jobuser.models import JobUser;
from random import randint;

class DetailView(TemplateView):
    template_name = 'pledge/detail.html';
    
    def get(self, request, *args, **kwargs):
        pledge = get_object_or_404(Pledge, random_string=kwargs['pledge_random_string']);
        return render(request, self.template_name, {'pledge': pledge});

class CreateView(TemplateView):
    template_name = 'pledge/create.html';
    pledge_form = PledgeForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        return render(request, self.template_name, {'job': job, 'form': self.pledge_form});
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        form = self.pledge_form(request.POST);
        if (form.is_valid()):
            amount = form.cleaned_data['amount'];
            comment = form.cleaned_data['comment'];
            jobuser = get_object_or_None(JobUser, user=request.user, job=job);
            if (jobuser is None):
                jobuser = JobUser(user=request.user, job=job);
            jobuser.pledged = jobuser.pledged + amount;
            jobuser.save();
            pledge = Pledge(jobuser=jobuser, amount=amount, comment=comment, random_string=createRandomString());
            pledge.save();
            job.pledged = job.pledged + amount;
            job.save();
            return redirect(job);
        else:
            return render(request, self.template_name, {'job': job, 'form': form});

@login_required            
def payment_confirmation(request, job_random_string):
    job = get_object_or_404(Job, random_string = job_random_string);
    context = {
        'job' : job,
    }
    return render(request, 'pledge/confirmation.html', context);
    
def createRandomString():
    random_string = '';
    available_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
    for i in range(50):
        index = randint(0, len(available_chars)-1);
        random_char = available_chars[index];
        random_string = random_string + random_char;
    if (Pledge.objects.filter(random_string=random_string).exists()):
        random_string = createRandomString();
    return random_string;
    