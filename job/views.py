from django.contrib.auth.decorators import login_required;
from django.shortcuts import render, get_object_or_404, redirect;
from .models import Job, Tag, User;
from jobuser.models import Update;
from jobuser.views import createUpdate;
from django.db.models import Q;
from jobuser.models import PledgeJob, WorkJob;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from django.contrib.auth import authenticate, login, logout;
from .forms import NewJobForm;
import json, re, math;
from random import randint;

@login_required
def home(request):
    context = {};
    jobs = Job.objects.none();
    sort_by = request.GET.get('sort-by');
    if (sort_by is not None):
        search = request.GET.get('search');
        if (search != ""):
            jobs = getJobs(search, sort_by, 0, 50);
    else:
        sort_by = 'created descending';
    context['jobs'] = jobs;
    context['sort_by'] = sort_by;        
    return render(request, 'job/home.html', context);
    
@login_required    
def see_more_jobs(request):
    if (request.is_ajax()):
        start = 50 * request.GET['numSearches'];
        end = start + 50;
        jobs = getJobs(request.GET['search'], request.GET['sort-by'], start, end);
        jobs = serializers.serialize('json', jobs);
        return HttpResponse(jobs, content_type="application/json");
    else:
        return Http404();
        
def getJobs(search, sort_by, start, end):
    search_array = search.split();
    jobs = Job.objects.all();
    for word in search_array:
        jobs = jobs.filter(Q(name__contains=word) | Q(tag__tag__contains=word)).distinct();
    sort_by_column = sort_by.split(" ")[0];
    ascending_or_descending = sort_by.split(" ")[1];
    if (sort_by_column == 'created'):
        if (ascending_or_descending == 'ascending'):
            jobs = jobs.order_by('creation_date');
        else:
            jobs = jobs.order_by('-creation_date');
    elif (sort_by == 'pledged'):
        if (ascending_or_descending == 'ascending'):
            jobs = jobs.order_by('money_pledged');
        else:
            jobs = jobs.order_by('-money_pledged');
    elif (sort_by == 'workers'):
        if (ascending_or_descending == 'ascending'):
            jobs = jobs.order_by('workers');
        else:
            jobs = jobs.order_by('-workers');
    else:
        if (ascending_or_descending == 'ascending'):
            jobs = jobs.order_by('name');
        else:
            jobs = jobs.order_by('-name');
    jobs = jobs[start:end];
    return jobs;

@login_required
def find_jobs_by_radius(jobs, currLatitude, currLongitude, radius):
    jobs = jobs.filter(latitude__range=(currLatitude - radius, currLatitude + radius));
    for job in jobs:
        lat = job.latitude;
        lon = job.longitude;
        distance = radius * math.acos(math.sin(currLatitude) * math.sin(lat) + math.cos(currLatitude) * math.cos(lat) * math.cos(math.fabs(currLongitude - lon))); #This is called the law of cosines to calculate distance on a sphere. (Earth is not a sphere, thus will have some margin of error. Computation speed compensates)
        if (distance > radius):
            jobs.exclude(id=job.id);
    return jobs;
    
@login_required    
def apply_tags_and_location(request):
    if (request.is_ajax()):
        data = {};
        jobs = [];
        if (request.method == 'GET'):
            typeOfTags = request.GET['typeOfTags'];
            if (typeOfTags == 'tag_basic_logic'):
                jobs = get_jobs_from_basic_tags(request.GET['basicTags']);
            else:
                tags = '';
                if (typeOfTags == 'tag_ANDs_of_ORs_logic'):
                    tags = request.user.userlogic.ANDs_of_ORs;
                elif (typeOfTags == 'tag_OR_of_ANDs_logic'):
                    tags = request.user.userlogic.ORs_of_ANDs;
                else:
                    tags = request.user.userlogic.custom;
                tags = apply_tags(tags);
                jobs = eval(tags).distinct();
            if (request.GET['locationTrue'] == 'true'):
                jobs = find_jobs_by_radius(jobs, float(request.GET['latitude']), float(request.GET['longitude']), float(request.GET['radius']));
            if (len(jobs) > 0):
                for i in range(len(jobs)):
                    job = jobs[i];
                    data['pk'] = job.pk;
                    data['name'] = job.name;
                    data['fields'] = {};
                    data['money_pledged'] = job.money_pledged;
                    data['num_workers'] = job.num_workers;
                data = apply_metrics_to_jobs(jobs);
        return JsonResponse(data, safe=False);
    else:
        return Http404();

@login_required
def get_jobs_from_basic_tags(tags):
    jobs = Job.objects.all();
    if (tags != ''):
        tagsArray = create_tags_array(tags);
        jobs = Job.objects.all();
        for tagString in tagsArray:       
            currtag = Tag.objects.get(tag__iexact=tagString);
            currJobs = currtag.jobs.all();
            jobs = jobs & currJobs;
    return jobs;
    
def apply_tags(tags):
    words = re.sub("[\W_]", " ",  tags).split();
    for word in words:
        if (not Tag.objects.filter(tag__iexact=word).exists()):
            Tag(tag=word).save();
    tags = re.sub(r'([a-zA-Z0-9]+)', "Tag.objects.get(tag__iexact='" + r'\1' + "').jobs.all()", tags);
    return tags;
    
def create_tags_array(tagsString):
    tagsString = tagsString.replace(","," ");
    return tagsString.split();

@login_required    
def detail(request, job_random_string):
    job = get_object_or_404(Job, random_string=job_random_string);
    if (request.method == "POST"):
        if ('pledge_money_to_job' in request.POST['pledge_money_to_job']):
            PledgeJob(pledger=request.user, job=job).save();
            return redirect('job:detail', job_random_string=job_random_string);
        elif ('work_on_job' in request.POST['work_on_job']):
            WorkJob(worker=request.user, job=job).save();
            return redirect('job:detail', job_random_string=job_random_string);
    pledgejob = None;
    workjob = None;
    if (request.user.pledgejob_set.all().filter(job=job).exists()):
        pledgejob = request.user.pledgejob_set.get(job=job);
    if (request.user.workjob_set.all().filter(job=job).exists()):
        workjob = request.user.workjob_set.get(job=job);
    context = {                                                                     
        'job': job,
        'pledgejob' : pledgejob,
        'workjob' : workjob,
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
def add_job(request):
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
            tagsArray = create_tags_array(tags);
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
    return render(request, 'job/add_job.html', context);
    
@login_required
def add_location(request):
    return render(request, 'job/add_location.html');
    
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
                   
                    
                    
    