from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect;
from .models import Job, Tag, User;
from jobuser.models import PledgeJob, WorkJob, WorkJobUpdate;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from django.contrib.auth import authenticate, login, logout;
from .forms import NewJobForm;
import json, re, math;

@login_required
def home(request):
    return render(request, 'job/home.html');

@login_required    
def search_jobs(request):
    if (request.is_ajax()):
        data = [];
        post_text = request.POST['job_name_or_id'];
        if post_text.isnumeric():
            post_text = int(post_text);
            data = Job.objects.get(pk=post_text);
            data = [data];
        else:
            post_text_array = post_text.split();
            data = Job.objects.all();
            for word in post_text_array:
                data = data.filter(name__contains=word);
        data = serializers.serialize("json", data);
        return HttpResponse(data, content_type="application/json");
    else:
        return Http404();

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
        jobs = Job.objects.all();                                               #       create a the variable data which starts out as all jobs
        for tagString in tagsArray :                                            #       for each individual tag the user inputted (gotten form the tags array variable)       
            currtag = Tag.objects.get(tag__iexact=tagString);                   #           find the tag from the database
            currJobs = currtag.jobs.all();                                      #           find all jobs, which contain the tag
            jobs = jobs & currJobs;           
    return jobs;
    
def apply_tags(tags):
    words = re.sub("[\W_]", " ",  tags).split();
    for word in words:
        if (not Tag.objects.filter(tag__iexact=word).exists()):
            Tag(tag=word).save();
    tags = re.sub(r'([a-zA-Z0-9]+)', "Tag.objects.get(tag__iexact='" + r'\1' + "').jobs.all()", tags);
    return tags;

@login_required    
def apply_metrics_to_jobs(jobs):
    for job in jobs:
        apply_pledge_metrics_to(job);
        apply_work_metrics_to(job);
    return jobs;
    
def apply_pledge_metrics_to(job):
    #amount_pledged = job.money_pledged;
    #filter = request.user.userpledgefilter;
    #for pledger in job.pledgejob_set.all():
    #    if (filter.inactive != '' && filter.inactive_unit != ''):
    #        ago = exec("datetime.timedelta(" + filter.inactive_unit + "=" + filter.inactive + ")");
    #        if (ago > pledger.lastlogin):
    #            amount_pledged = amount_pledged - pledger.amount_pledged;
    #    if (filter.failed_to_pay != ''):
    #        if (pledger):
    #            break;
    return None;
    
def create_tags_array(tagsString):
    tagsString = tagsString.replace(","," ");
    return tagsString.split();

@login_required    
def detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id);                                 
    is_main_editor = False;
    is_pledging = False;
    pledging_amount = 0;
    workjob = False;       
    if (request.user.pledgejob_set.all().filter(job=job).exists()):
        is_pledging = True;
        pledging_amount = request.user.pledgejob_set.get(job=job).amount_pledged;
    if (request.user.workjob_set.all().filter(job=job).exists()):
        workjob = request.user.workjob_set.get(job=job);
    context = {                                                                     
        'job': job,
        'workjob' : workjob,
        'is_pledging' : is_pledging,
        'pledging_amount' : pledging_amount,
        'workjob' : workjob,
        'ordered_updates' : WorkJobUpdate.objects.filter(workjob__job=job).order_by('updated'),
    }
    return render(request, 'job/detail.html', context);
    
@login_required
def view_workers(request, job_id):
    job = get_object_or_404(Job, pk=job_id);
    context = {
        'job' : job,
    }
    return render(request, 'job/view_workers.html', context);
    
@login_required    
def description(request, job_id):
    job = get_object_or_404(Job, pk=job_id);
    context = {
        'job': job,
    }
    return render(request, 'job/description.html', context);
    
@login_required    
def become_main_editor(request, job_id):
    job = get_object_or_404(Job, pk=job_id);
    if (request.method == 'POST'):
        if (job.main_editors.all().count() < 3):
            job.main_editors.add(request.user);
    return HttpResponse('Finished!');
    
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
def work_on_job(request, job_id):
    if (request.method == 'POST'):
        job = get_object_or_404(Job, pk=job_id);
        if (not job.workjob_set.filter(worker=request.user).exists()):
            WorkJob(worker=request.user, job=job).save();
    return HttpResponse('Finished!');

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
            job = Job(name=name, latitude=latitude, longitude=longitude, description=description);
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
            return redirect('/home');
    context = {
        'form' : NewJobForm(), 
    }
    return render(request, 'job/add_job.html', context);
    
@login_required
def add_location(request):
    return render(request, 'job/add_location.html');
    
    
    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
    