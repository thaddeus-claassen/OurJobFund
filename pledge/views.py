from django.shortcuts import render, render_to_response, get_object_or_404, redirect;
from .models import Job, Tag, UserLogic;
from django.http import JsonResponse, HttpResponse;
from django.core import serializers;
from django.contrib.auth import authenticate, login, logout;
from .forms import UserForm;
from django.views import generic;
from django.views.generic import View;
import json, re, math;

def index_pledge(request):
    return render(request, 'pledge/home_pledge.html');

def login_pledge(request):
    if (request.method == 'POST'):
        if (not request.user.is_authenticated()):
            email = request.POST.get('email');
            password = request.POST.get('password');
            user = authenticate(username=email, password=password);
            if user is not None:
                login(request, user);
    return index_pledge(request);

def logout_pledge(request):
    if (request.method == 'POST'):
        logout(request);
    return index_pledge(request);
    
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
    
def view_all_metrics_pledge(request):
    return render(request, 'pledge/view_all_metrics_pledge.html');
    
def apply_metrics_pledge(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            worker_database = request.user.userworkerfilter;
            worker_database.inactive = request.POST['inactive'];
            worker_database.inactive_unit = request.POST['inactive_unit_of_time'];
            worker_database.updated = request.POST['not-updated'];
            worker_database.updated_unit = request.POST['updated-unit-of-time'];
            worker_database.completed_fewer = request.POST['completed-fewer'];
            worker_database.failed_to_complete = request.POST['failed-to-complete'];
            worker_database.completed_percent = request.POST['completed-percent'];
            worker_database.better_than_complete_fail_ratio = request.POST['completed-ratio'];
            worker_database.save();
    return apply_metrics(request);
    
def clear_metrics(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            worker_database = request.user.userworkerfilter;
            worker_database.inactive = None;
            worker_database.inactive_unit = 'day';
            worker_database.updated = None;
            worker_database.updated_unit = 'day';
            worker_database.completed_fewer = None;
            worker_database.failed_to_complete = None;
            worker_database.completed_percent = None;
            worker_database.better_than_complete_fail_ratio = None;
            worker_database.save();
    return apply_metrics(request);

    
def apply_metrics(request):
    return render(request, 'pledge/home_pledge.html');
    
def apply_tags_and_location(request):
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
            latitude = float(request.GET['latitude']);
            longitude = float(request.GET['longitude']);
            radius = float(request.GET['radius']);
            jobs = find_jobs_by_radius(jobs, latitude, longitude, radius);
    jobs = serializers.serialize('json', jobs);
    return job_table(jobs);
                
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
    
def create_tags_array(tagsString):
    tagsString = tagsString.replace(","," ");
    return tagsString.split();

# Defines a function, which renders the HTML document ANDs_of_ORs.html
def ANDs_of_ORs(request):
    return render(request, 'pledge/ANDs_of_ORs.html');
    
def save_ANDs_of_ORs_tags(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            tags = request.POST['tags'];
            request.user.userlogic.ANDs_of_ORs = tags; 
            request.user.userlogic.save();
    return ANDs_of_ORs(request);
    
def get_ANDs_of_ORs_tags(request):
    tags = "";
    if (request.method == 'GET'):
        if (request.user.is_authenticated()):
            tags = request.user.userlogic.ANDs_of_ORs;
    return HttpResponse(tags);
            
def ORs_of_ANDs(request):
    return render(request, 'pledge/ORs_of_ANDs.html');
    
def save_ORs_of_ANDs_tags(request):
    if (request.method == 'POST'):
        if request.user.is_authenticated():
            tags = request.POST['tags'];
            request.user.userlogic.ORs_of_ANDs = tags; 
            request.user.userlogic.save();
    return ORs_of_ANDs(request);
    
def get_ORs_of_ANDs_tags(request):
    tags = "";
    if (request.method == 'GET'):
        if (request.user.is_authenticated()):
            tags = request.user.userlogic.ORs_of_ANDs;
    return HttpResponse(tags);
    
def custom(request):
    return render(request, 'pledge/custom.html');
    
def save_custom_tags(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            tags = request.POST.get('tags');
            request.user.userlogic.custom = tags; 
            request.user.userlogic.save();
    return custom(request);
    
def get_custom_tags(request):
    tags = "";
    if (request.method == 'GET'):
        if (request.user.is_authenticated()):
            tags = request.user.userlogic.custom;
    return HttpResponse(tags);

# Defines a function, which renders the HTML document detail.html (a.k.a. the page which opens when you click on a job link)
def detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id);                                        #Find the job from the given primary key, from inside the database
    all_tags = job.tag_set.all();                                           #Get all tags, which are used to describe the job
    context = {                                                                     #Define the context dictionary, which tells the HTML document what to call the given variables 
        'job': job,                                                                 #For detail.html, defines the string "job" as the given job
        'all_tags': all_tags,                                               #For detail.html, defines the string "all_tags" as the set of tags that are used to define the job
    }
    return render(request, 'pledge/detail.html', context);
    
def user_is_working_on_job(request, job_id):
    returnStatement = None;
    job = get_object_or_404(Job, pk=job_id);
    if (request.method == 'GET'):
        if (request.user.is_authenticated()):
            if (job.workers.filter(pk=request.user.pk).exists()):
                returnStatement = HttpResponse('Exists');
            else:
                returnStatement = HttpResponse('Does Not Exist');
    return returnStatement;
    
def work_on_job(request, job_id):
    returnStatement = None;
    job = get_object_or_404(Job, pk=job_id);
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            job.workers.add(request.user);
            returnStatement = HttpResponse('Exists'); 
    return returnStatement;

# Defines a function, which renders the HTML document add_job (a.k.a the page, which gives you the option to create a new job)
def add_job(request):
    return render(request, 'pledge/add_job.html');
    
def add_location(request):
    return render(request, 'pledge/add_location.html');
    
def create_job(request):
    if (request.method == 'POST'):
        name = request.POST['job_title'];
        latitude = request.POST['latitude'];
        longitude = request.POST['longitude'];
        description = request.POST['description'];
        job = Job(name=name, latitude=latitude, longitude=longitude, description=description);
        job.save();
        tags = request.POST['tags'];
        tagsArray = create_tags_array(tags);
        for tag in tagsArray :
            newTag = None;
            if (Tag.objects.filter(tag__iexact=tag).exists()):
                newTag = Tag.objects.get(tag__iexact=tag);
            else:
                newTag = Tag(tag=tag);
                newTag.save();
            job.tag_set.add(newTag);
    return add_job(request);
    
def description(request, job_id):
    job = get_object_or_404(Job, pk=job_id);
    context = {
        'job': job,
    }
    return render(request, 'pledge/job_description.html', context);
    
class UserFormView(View):
    form_class = UserForm;
    template_name = 'pledge/registration_form.html';
    
    # display blank form
    def get(self, request):
        form = self.form_class(None);
        return render(request, self.template_name, {'form': form});
        
    # process form data
    def post(self, request):
        form = self.form_class(request.POST);
        if form.is_valid():
            user = form.save(commit=False);
            # cleaned (normalized) data
            username = form.cleaned_data['username'];
            password = form.cleaned_data['password'];
            user.set_password(password);
            user.save();
            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password);
            if user is not None:
                if user.is_active:
                    login(request, user);
                    return redirect('pledge:index');
        return render(request, self.template_name, {'form': form});
                    
    