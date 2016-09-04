from django.shortcuts import render, get_object_or_404
from .models import Job


def index(request):
    all_jobs = Job.objects.all()
    return render(request, 'jobList_Pledge/index.html', {'all_jobs': all_jobs})

def detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'jobList_Pledge/detail.html', {'job': job})
