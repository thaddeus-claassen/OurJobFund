from django.shortcuts import render, get_object_or_404
from .models import Job


def index(request):
#    num_jobs = Job.objects.all().count
#    min = 0
#    if numJobs > 1000:
#        min = num_jobs - 1000
#    all_jobs = Job.objects.all()[min:num_jobs]
    all_jobs = Job.objects.all()
    context = {
        'all_jobs': all_jobs,
    }
    return render(request, 'jobList_Pledge/index.html', context)

def detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    all_hashtags = job.hashtag_set.all()
    context = {
        'job': job,
        'all_hashtags': all_hashtags,
    }
    return render(request, 'jobList_Pledge/detail.html', context)

def add_job(request):
    return render(request, 'jobList_Pledge/add_job.html')
