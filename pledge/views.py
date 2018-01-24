from django.contrib.auth.decorators import login_required;
from django.shortcuts import render, get_object_or_404;
from job.models import Job;

@login_required
def payment_confirmation(request, job_random_string):
    job = get_object_or_404(Job, random_string = job_random_string);
    context = {
        'job' : job,
    }
    return render(request, 'pledge/confirmation.html', context);