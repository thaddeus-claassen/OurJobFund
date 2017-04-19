from django.shortcuts import render, get_object_or_404, redirect;
from .models import Job, Tag, User;
from jobuser.models import PledgeJob, WorkJob, WorkJobUpdate;
from django.http import JsonResponse, HttpResponse;
from django.core import serializers;
from django.contrib.auth import authenticate, login, logout;
from .forms import NewJobForm;
import json, re, math;    
    
def pledge(request):
    return render(request, 'job/pledge.html');
    
def work(request):
    return render(request, 'job/work.html');

def login_pledge(request):
    if (request.method == 'POST'):
        if (not request.user.is_authenticated()):
            email = request.POST.get('email');
            password = request.POST.get('password');
            user = authenticate(username=email, password=password);
            if user is not None:
                login(request, user);
    return pledge(request);

def logout_pledge(request):
    if (request.method == 'POST'):
        logout(request);
    return pledge(request);
    
# This subroutine returns the JSON objects for the main job table in index.html
def job_table(jobs):
    return HttpResponse(                                        #Returns the HttpResponse as a JSON object for the main job table 
            jobs,                                               #   Names the object we want to send as JSON
            content_type="application/json",                    #   For some reason, we have to say this line. I guess so whatever reads this response knows its a JSON object
        );
        
# This gets the any jobs which match the name or id search in index.html
def search_jobs(request):    
    data = [];
    if (request.method == 'POST'):                               #if the request was a POST (I don't know why I'm supposed to do this, only the POST request from the search bar should calls method)
        post_text = request.POST['job_name_or_id'];              #   set post_text variable to the user's query
        if post_text.isnumeric():                                #   check if the query is a number
            post_text = int(post_text);                          #       if it is, set the variable to a python integer
            data = Job.objects.get(pk=post_text);                #       then get the job whose ID is that integer
            data = [data];
        else:                                                    #   if it's not a number
            post_text_array = post_text.split();                 #       hold each word from the user's query in a temporary array
            data = Job.objects.all();
            for word in post_text_array:                         #       for each word the user used to search
                data = data.filter(name__contains=word);         #           filter out any job which does not include that word    
    data = serializers.serialize("json", data);              
    return job_table(data);                                      #call the job_table subroutine, which will hopefully put the jobs the user searched into the table
    
def find_jobs_by_radius(jobs, currLatitude, currLongitude, radius):
    jobs = jobs.filter(latitude__range=(currLatitude - radius, currLatitude + radius));
    for job in jobs:
        lat = job.latitude;
        lon = job.longitude;
        distance = radius * math.acos(math.sin(currLatitude) * math.sin(lat) + math.cos(currLatitude) * math.cos(lat) * math.cos(math.fabs(currLongitude - lon))); #This is called the law of cosines to calculate distance on a sphere. (Earth is not a sphere, thus will have some margin of error. Computation speed compensates)
        if (distance > radius):
            jobs.exclude(id=job.id);
    return jobs;
    
def view_all_metrics_pledge(request, user_id):
    user = get_object_or_404(User, pk=user_id);
    context = {
        'form' : ApplyPledgeMetricsForm(initial=getUserWorkerFilterData(user)),
        'username' : user.username,
        'pledge_metrics' : user.userworkerfilter,
    }
    return render(request, 'job/view_all_metrics_pledge.html', context);
    
def view_all_metrics_work(request, user_id):
    user = get_object_or_404(User, pk=user_id);
    context = {
        'form' : ApplyWorkMetricsForm(initial=getUserPledgeFilterData(user)),
        'username' : user.username,
        'work_metrics' : user.userpledgefilter,
    }
    return render(request, 'job/view_all_metrics_work.html', context);
    
def apply_metrics(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            type = request.POST.get('type');
            if (type == 'pledge'):
                pledgeMetricForm = ApplyPledgeMetricsForm(data=request.POST, instance=request.user.userworkerfilter);
                if (pledgeMetricForm.is_valid()):
                    pledgeMetricForm.save();
                    return render(request, 'job/pledge.html');
            else:
                workMetricForm = ApplyWorkMetricsForm(data=request.POST, instance=request.user.userpledgefilter);
                if (workMetricForm.is_valid()):
                    workMetricForm.save();
                    return render(request, 'job/work.html');
    
def clear_metrics(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            database = request.POST['pledge_or_worker'];
            if (database == 'pledge-page-worker-database'):
                return clear_work_metrics(request, pledgeMetricForm);
            else:
                return clear_pledge_metrics(request, request.user.userpledgefilter);
    return render(request, 'job/pledge.html');  

def clear_pledge_metrics(request, pledge_database):
    pledge_database.inactive = None;
    pledge_database.inactive_unit = 'day';
    pledge_database.failed_to_pay = None;
    pledge_database.averaged = None;
    pledge_database.paid_x_times = None;
    return HttpResponse("Pledge Metrics Cleared");

def clear_work_metrics(request, form):
    worker_database.inactive = None;
    worker_database.inactive_unit = 'day';
    worker_database.updated = None;
    worker_database.updated_unit = 'day';
    worker_database.completed_fewer = None;
    worker_database.failed_to_complete = None;
    worker_database.completed_percent = None;
    worker_database.better_than_complete_fail_ratio = None;
    worker_database.save();
    return HttpResponse("Work Metrics Cleared");
    
def apply_tags_and_location(request):
    data = {};
    jobs = [];
    if (request.method == 'GET'):
        if (request.user.is_authenticated()):
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
        else:
            jobs = get_jobs_from_basic_tags(request.GET['basicTags']);
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

def detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id);                                 
    is_main_editor = False;
    is_pledging = False;
    pledging_amount = 0;
    workjob = False;       
    if (request.user.is_authenticated()):
        if (request.user.main_editors.filter(pk=job_id).exists()):
            is_main_editor = True;
        if (request.user.pledgejob_set.all().filter(job=job).exists()):
            is_pledging = True;
            pledging_amount = request.user.pledgejob_set.get(job=job).amount_pledged;
        if (request.user.workjob_set.all().filter(job=job).exists()):
            workjob = request.user.workjob_set.get(job=job);
    context = {                                                                     
        'job': job,
        'workjob' : workjob,
        'is_main_editor' : is_main_editor,
        'is_pledging' : is_pledging,
        'pledging_amount' : pledging_amount,
        'workjob' : workjob,
        'ordered_updates' : WorkJobUpdate.objects.filter(workjob__job=job).order_by('updated'),
    }
    return render(request, 'job/detail.html', context);
    
def view_workers(request, job_id):
    job = get_object_or_404(Job, pk=job_id);
    context = {
        'job' : job,
    }
    return render(request, 'job/view_workers.html', context);
    
def description(request, job_id):
    job = get_object_or_404(Job, pk=job_id);
    context = {
        'job': job,
    }
    return render(request, 'job/description.html', context);
    
def become_main_editor(request, job_id):
    job = get_object_or_404(Job, pk=job_id);
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            if (job.main_editors.all().count() < 3):
                job.main_editors.add(request.user);
    return HttpResponse('Finished!');
    
def pledge_money_to_job(request, job_id):
    string = "";
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            job = get_object_or_404(Job, pk=job_id);
            if (not job.pledgejob_set.filter(pledger=request.user).exists()):
                amount_pledged = float(request.POST['amount_pledged']);
                PledgeJob(pledger=request.user, job=job, amount_pledged=amount_pledged).save();
                job.money_pledged = job.money_pledged + amount_pledged;
                job.save();
                string += request.user.username + " " + amount_pledged; 
    return HttpResponse(string);
    
def work_on_job(request, job_id):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            job = get_object_or_404(Job, pk=job_id);
            if (not job.workjob_set.filter(worker=request.user).exists()):
                WorkJob(worker=request.user, job=job).save();
    return HttpResponse('Finished!');

# Defines a function, which renders the HTML document add_job (a.k.a the page, which gives you the option to create a new job)
def add_job(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            newJobForm = NewJobForm(request.POST);
            if (newJobForm.is_valid()):
                name = newJobForm.cleaned_data['name'];
                latitude = newJobForm.cleaned_data['latitude'];
                longitude = newJobForm.cleaned_data['longitude'];
                tags = newJobForm.cleaned_data['tags'];
                description = newJobForm.cleaned_data['description'];
                job = Job(name=name, latitude=latitude, longitude=longitude, description=description);
                job.save();
                job.main_editors.add(request.user);
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
    
def add_location(request):
    return render(request, 'job/add_location.html');
    
def verify_username(request):
    userNameExists = None;
    if (request.method == 'GET'):
        username = request.GET['username'];
        if (User.objects.filter(username__iexact=username).exists()):
            userNameExists = 'true';
        else:
            userNameExists = 'false';
    return HttpResponse(userNameExists);   
    
def copy_pledge_metrics(request):
    data = {};
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            otherUser = User.objects.get(username=request.POST['username']);
            copy_pledge_filter(request.user, otherUser);
            data = getUserWorkerFilterData(otherUser);
    return JsonResponse(data, safe=False);
    
def copy_worker_metrics(request):
    data = {};
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            otherUser = User.objects.get(username=request.POST['username']);
            copy_worker_filter(request.user, otherUser);
            data = getUserPledgeFilterData(otherUser);
    return JsonResponse(data, safe=False);
    
def copy_pledge_filter_job(user, otherUser):
    user.userworkerfilter.inactive = otherUser.userworkerfilter.inactive;
    user.userworkerfilter.inactive_unit = otherUser.userworkerfilter.inactive_unit;
    user.userworkerfilter.updated = otherUser.userworkerfilter.updated;
    user.userworkerfilter.updated_unit = otherUser.userworkerfilter.updated_unit;
    user.userworkerfilter.completed_fewer = otherUser.userworkerfilter.completed_fewer;
    user.userworkerfilter.failed_to_complete = otherUser.userworkerfilter.failed_to_complete;
    user.userworkerfilter.completed_percent = otherUser.userworkerfilter.completed_percent;
    user.userworkerfilter.completed_ratio = otherUser.userworkerfilter.completed_ratio;
    user.userworkerfilter.save();
    
def copy_worker_filter_job(user, otherUser):
    user.userpledgefilter.inactive = otherUser.userpledgefilter.inactive;
    user.userpledgefilter.inactive_unit = otherUser.userpledgefilter.inactive_unit;
    user.userpledgefilter.failed_to_pay = otherUser.userpledgefilter.failed_to_pay;
    user.userpledgefilter.averaged = otherUser.userpledgefilter.averaged;
    user.userpledgefilter.paid_x_times = otherUser.userpledgefilter.paid_x_times;
    user.userpledgefilter.save();
    
def getUserWorkerFilterData(user):
    data = {};
    data['inactive'] = user.userworkerfilter.inactive;
    data['inactive_unit'] = user.userworkerfilter.inactive_unit;
    data['updated'] = user.userworkerfilter.updated;
    data['updated_unit'] = user.userworkerfilter.updated_unit;
    data['completed_fewer'] = user.userworkerfilter.completed_fewer;
    data['failed_to_complete'] = user.userworkerfilter.failed_to_complete;
    data['completed_percent'] = user.userworkerfilter.completed_percent;
    data['completed_ratio'] = user.userworkerfilter.completed_ratio;
    return data;
    
def getUserPledgeFilterData(user):
    data = {};
    data['inactive'] = user.userpledgefilter.inactive;
    data['inactive_unit'] = user.userpledgefilter.inactive_unit;
    data['failed_to_pay'] = user.userpledgefilter.failed_to_pay;
    data['averaged'] = user.userpledgefilter.averaged;
    data['paid_x_times'] = user.userpledgefilter.paid_x_times;
    return data;
    
    
    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
    