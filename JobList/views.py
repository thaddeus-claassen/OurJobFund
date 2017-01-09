from django.shortcuts import render, render_to_response, get_object_or_404, redirect;
from .models import Job, Tag, UserLogic;
from django.http import JsonResponse, HttpResponse;
from django.core import serializers;
from django.contrib.auth import authenticate, login;
from .forms import UserForm;
from django.views import generic;
from django.views.generic import View;
import json, re, math;

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
    
def search_jobs_by_radius(request):
    data = [];
    if (request.method == 'POST'):
        currLatitude = float(request.POST['latitude']);
        currLongitude = float(request.POST['longitude']);
        radius = float(request.POST['radius']);
        data = find_jobs_by_radius(Job.objects.all(), currLatitude, currLongitude, radius);
    data = serializers.serialize("json", data);
    return job_table(data);
    
def find_jobs_by_radius(jobs, currLatitude, currLongitude, radius):
    data = Job.objects.filter(latitude__range=(currLatitude - radius, currLatitude + radius));
    for job in data:
        lat = job.latitude;
        lon = job.longitude;
        distance = radius * math.acos(math.sin(currLatitude) * math.sin(lat) + math.cos(currLatitude) * math.cos(lat) * math.cos(math.fabs(currLongitude - lon))); #This is called the law of cosines to calculate distance on a sphere. (Earth is not a sphere, thus will have some margin of error. Computation speed compensates)
        if (distance > radius):
            data.exclude(id=job.id);
    return data;
    
def view_all_metrics_pledge(request):
    return render(request, 'JobList/view_all_metrics_pledge.html');
    
def apply_metrics(request):
    return render(request, 'JobList/home_logged_out_pledge.html');
    
# Defines the function which finds the jobs which correspond to the basic tag input
def apply_basic_tags(request):
    data = [];
    if (request.method == 'POST'):                                                  #if the request was a POST (again, I am not entirely sure why I should use this if statement)
        tags = request.POST['tags'];                                       #   set the post_text variable to the list of tags the user inputted
        if (tags != ''):                                                       #   if post_text contains something
            tagsArray = create_tags_array(tags);                       #       create a tags array and set each tag the user inputted as an element to the array
            data = get_jobs_from_basic_tags(tagsArray);                                 #           change the data variable so it doesn't contain jobs without the tag (we do this by taking the intersection of the jobs, which contain the tag and the set of jobs previously contained by the prior data variable)
    data = serializers.serialize("json", data);                                     #Change the data variable so it can be read as a JSON object
    return job_table(data);
    
def apply_tag_basic_logic_and_location(request):
    data = [];
    if (request.method == 'GET'):
        tags = request.GET['tags'];
        if (tags == ''):
            data = Job.objects.all();
        else:
            tagsArray = create_tags_array(tags);
            data = get_jobs_from_basic_tags(tagsArray);
        latitude = float(request.GET['latitude']);
        longitude = float(request.GET['longitude']);
        radius = float(request.GET['radius']);
        find_jobs_by_radius(data, latitude, longitude, radius);
    return data;
        
        
def apply_tag_basic_logic(request):
    data = [];
    if (request.method == "GET"):
        if (requested.user.is_authenticated()):
            tags = request.GET['tags'];
            tagsArray = create_tags_array(tags);
            data = get_jobs_from_basic_tags(tagsArray);
    data = serializers.serialize("json", data);
    return job_table(data)
                
def get_jobs_from_basic_tags(tagsArray):
    jobs = Job.objects.all();                                               #       create a the variable data which starts out as all jobs
    for tagString in tagsArray :                                    #       for each individual tag the user inputted (gotten form the tags array variable)       
        currtag = Tag.objects.get(tag__iexact=tagString);   #           find the tag from the database
        currJobs = currtag.jobs.all();                                  #           find all jobs, which contain the tag
        jobs = jobs & currJobs;           
    return jobs;

def apply_tag_ANDs_of_ORs_logic(request):
    data = [];
    if (request.method == "GET"):
        if (request.user.is_authenticated()):
            tags = request.user.userlogic.ANDs_of_ORs;
            tags = apply_tags(tags);
            data = eval(tags);
    data = serializers.serialize("json", data);
    return job_table(data);
    
def apply_tag_ORs_of_ANDs_logic(request):
    data = [];
    if (request.method == "GET"):
        if (request.user.is_authenticated()):
            tags = request.user.userlogic.ORs_of_ANDs;
            print(tags);
            tags = apply_tags(tags);
            print(tags);
            data = eval(tags);
    data = serializers.serialize("json", data);
    return job_table(data);
    
def apply_tag_custom_logic(request):
    data = [];
    if (request.method == "GET"):
        if (request.user.is_authenticated()):
            tags = request.user.userlogic.custom;
            tags = apply_tags(tags);
            data = eval(tags);
    data = serializers.serialize("json", data);
    return job_table(data);
    
def apply_tags(tags):
    words = re.sub("[\W_]", " ",  tags).split();
    for word in words:
        if (not Tag.objects.filter(tag__iexact=word).exists()):
            Tag(tag=word).save();
    tags = re.sub(r'([a-zA-Z0-9]+)', "Tag.objects.get(tag__iexact='" + r'\1' + "').jobs.all()", tags);
    return tags;
    
def create_tags_array(tagsString):
    tagsString = tagsString.replace(" ","");
    return tagsString.split(",");

# Defines a function, which renders the HTML document ANDs_of_ORs.html
def ANDs_of_ORs(request):
    return render(request, 'JobList/ANDs_of_ORs.html');
    
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
    return render(request, 'JobList/ORs_of_ANDs.html');
    
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
    return render(request, 'JobList/custom.html');
    
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
    
#def index(request):
#    returnRender = None;
#    if (request.user.is_authenticated()):
#        return render(request, 'JobList/home_logged_in_pledge.html');
#    else:
#        return render(request, 'JobList/home_logged_out_pledge.html');

# Defines a function, which renders the HTML document index.html (a.k.a. the main JobList page)
def index(request):
    return render(request, 'JobList/home_logged_out_pledge.html');

# Defines a function, which renders the HTML document detail.html (a.k.a. the page which opens when you click on a job link)
def detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id);                                        #Find the job from the given primary key, from inside the database
    all_tags = job.tag_set.all();                                           #Get all tags, which are used to describe the job
    context = {                                                                     #Define the context dictionary, which tells the HTML document what to call the given variables 
        'job': job,                                                                 #For detail.html, defines the string "job" as the given job
        'all_tags': all_tags,                                               #For detail.html, defines the string "all_tags" as the set of tags that are used to define the job
    }
    return render(request, 'JobList/detail.html', context)

# Defines a function, which renders the HTML document add_job (a.k.a the page, which gives you the option to create a new job)
def add_job(request):
    return render(request, 'JobList/add_job.html');
    
def add_location(request):
    return render(request, 'JobList/add_location.html');
    
def create_job(request):
    if (request.method == 'POST'):
        name = request.POST.get('job_title');
        latitude = request.POST.get('latitude');
        longitude = request.POST.get('longitude');
        tags = request.POST.get('create_tags');
        description = request.POST.get('description');
        job = Job(name=name, latitude=latitude, longitude=longitude, description=description);
        job.save();
        tagsArray = create_tags_array(tags);
        for tag in tagsArray :
            newTag = None;
            if (Tag.objects.filter(tag__iexact=tag).exists()):
                newTag = Tag.objects.get(tag__iexact=tag);
            else:
                newTag = Tag(tag=tag);
                newTag.save();
            job.tag_set.add(newTag);
    return index(request);
    
def description(request, job_id):
    job = get_object_or_404(Job, pk=job_id);
    context = {
        'job': job,
    }
    return render(request, 'JobList/job_description.html', context);
    
class UserFormView(View):
    form_class = UserForm;
    template_name = 'JobList/registration_form.html';
    
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
                    return redirect('JobList:index');
        return render(request, self.template_name, {'form': form});
                    
    