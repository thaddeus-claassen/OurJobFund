from django.contrib.auth.decorators import login_required;
from django.shortcuts import render, get_object_or_404, redirect;
from .models import Job, Tag, User;
from jobuser.models import Update;
from jobuser.views import createUpdate;
from django.db.models import Q;
from jobuser.models import JobUser;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from django.contrib.auth import authenticate, login, logout;
from .forms import NewJobForm;
import json, re, math;
from random import randint;

@login_required
def home(request):     
    return render(request, 'job/home.html');
    
@login_required
def get_jobs(request):
    if (request.is_ajax()):
        jobs = findJobs(request);
        jobs = jobs[0:50];
        jobs = serializers.serialize('json', jobs);
        return HttpResponse(jobs, content_type="application/json");
    else:
        return Http404();

@login_required
def add_jobs(request):
    if (request.is_ajax()):
        numSearches =  int(request.GET['numSearches']);
        jobs = findJobs(request);
        jobs = jobs[50 * numSearches:50 * (numSearches + 1)];
        jobs = serializers.serialize('json', jobs);
        return HttpResponse(jobs, content_type="application/json");
    else:
        return Http404();

@login_required        
def sort_jobs(request):
    if (request.is_ajax()):
        numSearches =  int(request.GET['numSearches']);
        jobs = findJobs(request);
        jobs = jobs[0:50 * numSearches];
        jobs = serializers.serialize('json', jobs);
        return HttpResponse(jobs, content_type="application/json");
    else:
        return Http404();
        
@login_required
def get_total_jobs(request):
    if (request.is_ajax()):
        jobs = findJobs(request);
        total = {};
        total['total'] = jobs.count();
        return HttpResponse(json.dumps(total), content_type="application/json");
    else:
        return Http404();
        
def findJobs(request):
    search_array = request.GET['search'].split(" "); 
    sort_array = request.GET['sort'].split(" ");
    latitude_in_degrees_as_string = request.GET['latitude'];
    longitude_in_degrees_as_string = request.GET['longitude'];
    radius_in_miles_as_string = request.GET['radius'];
    jobs = Job.objects.all();
    if (latitude_in_degrees_as_string != "" and longitude_in_degrees_as_string != "" and radius_in_miles_as_string != ""):
        jobs = findJobsByRadius(jobs, float(latitude_in_degrees_as_string), float(longitude_in_degrees_as_string), float(radius_in_miles_as_string));
    for word in search_array:
        jobs = jobs.filter(Q(name__contains=word) | Q(tag__tag__contains=word));
    jobs = jobs.distinct();
    if (sort_array[0] == 'created'):
        if (sort_array[1] == 'ascending'):
            jobs = jobs.order_by('creation_date');
        else:
            jobs = jobs.order_by('-creation_date');
    elif (sort_array[0] == 'pledged'):
        if (sort_array[1] == 'ascending'):
            jobs = jobs.order_by('money_pledged');
        else:
            jobs = jobs.order_by('-money_pledged');
    elif (sort_array[0] == 'workers'):
        if (sort_array[1] == 'ascending'):
            jobs = jobs.order_by('workers');
        else:
            jobs = jobs.order_by('-workers');
    else:
        if (sort_array[1] == 'ascending'):
            jobs = jobs.extra(select={'case_insensitive_name': 'lower(name)'}).order_by('case_insensitive_name');
        else:
            jobs = jobs.extra(select={'case_insensitive_name': 'lower(name)'}).order_by('-case_insensitive_name');
    return jobs;

def findJobsByRadius(jobs, latitude_in_degrees, longitude_in_degrees, radius_in_miles):
    radius_in_degrees = radius_in_miles / 69;
    latitude_in_radians = latitude_in_degrees * math.pi / 180;
    longitude_in_radians = longitude_in_degrees * math.pi / 180;
    radius_in_radians = radius_in_degrees * math.pi / 180;
    jobs = jobs.filter(latitude__range=(latitude_in_degrees - radius_in_degrees, latitude_in_degrees + radius_in_degrees));
    for job in jobs:
        lat = job.latitude * math.pi / 180;
        lon = job.longitude * math.pi / 180;
        RADIUS_OF_EARTH_IN_MILES = 3959;
        distance = RADIUS_OF_EARTH_IN_MILES * math.acos(math.sin(latitude_in_radians) * math.sin(lat) + math.cos(latitude_in_radians) * math.cos(lat) * math.cos(math.fabs(longitude_in_radians - lon))); #This is called the Spherical Law of Cosines and it is used to calculate distances on a sphere. (Note: Earth is not a sphere, thus this will have a margin of error, but it is small. Computation speed compensates)
        print("Job: " + job.name + " Distance: " + str(distance));
        if (distance > radius_in_miles):
            print("Excluded Job: " + job.name);
            jobs = jobs.exclude(id=job.id);
    return jobs;

@login_required    
def detail(request, job_random_string):
    job = get_object_or_404(Job, random_string=job_random_string);
    if (request.method == "POST"):
        jobuser = JobUser.objects.filter(user=request.user, job=job).first();
        if (not jobuser):
            jobuser = JobUser(user=request.user, job=job).save();
        if ('pledge_money_to_job' in request.POST):
            pass;
        elif ('pay_money_to_job' in request.POST):
            pass;
        elif ('work_on_job' in request.POST):
            work = Work(jobuser=jobuser);
            finish.save();
        elif ('finish_job' in request.POST):
            finish = Finish(jobuser=jobuser);
            finish.save()
        return redirect('job:detail', job_random_string=job_random_string);
    jobuser = None;
    if (JobUser.objects.filter(user=request.user, job=job).exists()):
        jobuser = request.user.jobuser_set.all().get(job=job);
    context = {                                                                     
        'job': job,
        'jobuser' : jobuser,
        'ordered_updates' : Update.objects.all(),
    }
    return render(request, 'job/detail.html', context);
    
@login_required
def pledge_money_to_job(request, job_id):
    string = "";
    if (request.method == 'POST'):
        job = get_object_or_404(Job, pk=job_id);
        if (not job.pledgejob_set.filter(pledger=request.user).exists()):
            amount_pledged = float(request.POST['amount_pledged']);
            PledgeJob(pledger=request.user, job=job, amount_pledged=amount_pledged).save();
            job.money_pledged = job.money_pledged + amount_pledged;
            job.save();
            string += request.user.username + " " + amount_pledged; 
    return HttpResponse(string);
    
@login_required
def work_on_job(request, job_random_string):
    return_string = "Did not go through normal AJAX call";
    if (request.method == 'POST'):
        job = get_object_or_404(Job, random_string=job_random_string);
        if (not job.workjob_set.filter(worker=request.user).exists()):
            workjob = WorkJob(worker=request.user, job=job).save();
            return_string = "success";
    return HttpResponse(return_string);

@login_required    
def create_job(request):
    if (request.method == 'POST'):
        newJobForm = NewJobForm(request.POST);
        if (newJobForm.is_valid()):
            name = newJobForm.cleaned_data['name'];
            latitude = newJobForm.cleaned_data['latitude'];
            longitude = newJobForm.cleaned_data['longitude'];
            tags = newJobForm.cleaned_data['tags'];
            description = newJobForm.cleaned_data['description'];
            job = Job(name=name, latitude=latitude, longitude=longitude, description=description, random_string=createRandomString());
            job.save();
            tags = request.POST['tags'];
            tagsArray = tags.split(" ");
            for tagString in tagsArray:
                newTag = None;
                if (Tag.objects.filter(tag__iexact=tagString).exists()):
                    newTag = Tag.objects.get(tag__iexact=tagString);
                else:
                    newTag = Tag(tag=tagString);
                newTag.save();
                job.tag_set.add(newTag);
            return redirect('job:home');
    context = {
        'form' : NewJobForm(), 
    }
    return render(request, 'job/create_job.html', context);
    
def createRandomString():
    random_string = '';
    available_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
    for i in range(50):
        index = randint(0, 61);
        random_char = available_chars[index];
        random_string = random_string + random_char;
    if (Job.objects.filter(random_string=random_string).exists()):
        random_string = createRandomString();
    return random_string;
                   
                    
                    
    