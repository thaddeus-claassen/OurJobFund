from django.shortcuts import render, render_to_response, get_object_or_404, redirect;
from .models import Job, Hashtag;
from django.http import JsonResponse, HttpResponse;
from django.core import serializers;
from django.contrib.auth import authenticate, login;
from .forms import UserForm;
from django.views import generic;
from django.views.generic import View;
import json;
import math;

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
        randomJobs = Job.objects.all();
        data = Job.objects.filter(latitude__range=(currLatitude - radius, currLatitude + radius));
        for job in data:
            lat = job.latitude;
            lon = job.longitude;
            distance = radius * math.acos(math.sin(currLatitude) * math.sin(lat) + math.cos(currLatitude) * math.cos(lat) * math.cos(math.fabs(currLongitude - lon))); #This is called the law of cosines to calculate distance on a sphere. (Earth is not a sphere, thus will have some margin of error. Computation speed compensates)
            if (distance > radius):
                data.exclude(id=job.id);
    data = serializers.serialize("json", data);
    return job_table(data);
    
   
def view_all_metrics_pledge(request):
    return render(request, 'jobList_Pledge/view_all_metrics_pledge.html');
    
def apply_metrics(request):
    return render(request, 'jobList_Pledge/index.html');
    
# Defines the function which finds the jobs which correspond to the basic hashtag input
def apply_basic_hashtags(request):
    data = [];
    if (request.method == 'POST'):                                                  #if the request was a POST (again, I am not entirely sure why I should use this if statement)
        post_text = request.POST['hashtags'];                                       #   set the post_text variable to the list of hashtags the user inputted
        if (post_text != ''):                                                       #   if post_text contains something
            hashtagsArray = create_hashtags_array(post_text);                                 #       create a hashtags array and set each hashtag the user inputted as an element to the array
            data = Job.objects.all();                                               #       create a the variable data which starts out as all jobs
            print("Num jobs: " + str(len(data)));
            for hashtagString in hashtagsArray :                                    #       for each individual tag the user inputted (gotten form the hashtags array variable)       
                currHashtag = Hashtag.objects.get(hashtag__iexact=hashtagString);   #           find the hashtag from the database
                currJobs = currHashtag.jobs.all();                                  #           find all jobs, which contain the hashtag
                data = data & currJobs;                                             #           change the data variable so it doesn't contain jobs without the hashtag (we do this by taking the intersection of the jobs, which contain the tag and the set of jobs previously contained by the prior data variable)
    data = serializers.serialize("json", data);                                     #Change the data variable so it can be read as a JSON object
    return job_table(data);
    
def create_hashtags_array(hashtagsString):
    hashtagsString = hashtagsString.replace(" ","");
    return hashtagsString.split(",");

# Defines a function, which renders the HTML document ANDs_of_ORs.html
def ANDs_of_ORs(request):
    return render(request, 'jobList_Pledge/ANDs_of_ORs.html');
    
def custom_logic(request):
    return render(request, 'jobList_Pledge/custom_logic.html');

# Defines a function, which renders the HTML document index.html (a.k.a. the main jobList_Pledge page)
def index(request):
    return render(request, 'jobList_Pledge/index.html');

# Defines a function, which renders the HTML document detail.html (a.k.a. the page which opens when you click on a job link)
def detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id);                                        #Find the job from the given primary key, from inside the database
    all_hashtags = job.hashtag_set.all();                                           #Get all hashtags, which are used to describe the job
    context = {                                                                     #Define the context dictionary, which tells the HTML document what to call the given variables 
        'job': job,                                                                 #For detail.html, defines the string "job" as the given job
        'all_hashtags': all_hashtags,                                               #For detail.html, defines the string "all_hashtags" as the set of hashtags that are used to define the job
    }
    return render(request, 'jobList_Pledge/detail.html', context)

# Defines a function, which renders the HTML document add_job (a.k.a the page, which gives you the option to create a new job)
def add_job(request):
    return render(request, 'jobList_Pledge/add_job.html');
    
def create_job(request):
    if (request.method == 'POST'):
        name = request.POST.get('job_title');
        latitude = request.POST.get('latitude');
        longitude = request.POST.get('longitude');
        hashtags = request.POST.get('create_tags');
        description = request.POST.get('description');
        job = Job(name=name, latitude=latitude, longitude=longitude, description=description);
        job.save();
        hashtagsArray = create_hashtags_array(hashtags);
        for tag in hashtagsArray :
            newTag = None;
            if (Hashtag.objects.filter(hashtag__iexact=tag).exists()):
                newTag = Hashtag.objects.get(hashtag__iexact=tag);
            else:
                newTag = Hashtag(hashtag=tag);
                newTag.save();
            job.hashtag_set.add(newTag);
    return index(request);
    
def description(request, job_id):
    job = get_object_or_404(Job, pk=job_id);
    context = {
        'job': job,
    }
    return render(request, 'jobList_Pledge/job_description.html', context);

def apply_hashtags(request):
    jobs = [];
    if (request.method == 'POST'):
        hashtags = request.POST['hashtags'];
        jobs = replaceStringWithJobs(hashtags);
        jobs = Job.objects.all() & jobs;
    jobs = serializers.serialize("json", jobs);
    print(jobs)
    return job_table(jobs);
    
def replaceStringWithJobs(hashtags):
    startIndex = -1;
    currIndex = 0;
    moreHashtagsToConvert = True;
    while (moreHashtagsToConvert):
        char = hashtags[currIndex];
        if (char == '#'):
            startIndex = currIndex + 1;
            isAlphanumeric = True;
            while (isAlphanumeric):
                currIndex = currIndex + 1;
                char = hashtags[currIndex];
                isAlphanumeric = char.isalnum();
            hashtags = replaceWordForJobs(hashtags, startIndex, currIndex - 1);
        currIndex = currIndex + 1;
    return eval(hashtags);
    
def replaceWordForJobs(hashtags, startIndex, endIndex):
    partOne = hashtags[0:startIndex];
    partTwo = "Hashtag.objects.get(hashtags__iexact=" + hashtags[startIndex + 1:endIndex] + ").jobs.all()";
    partThree = hashtags[endIndex:hashtags.len()];
    return (partOne + partTwo + partThree);

    
class UserFormView(View):
    form_class = UserForm;
    template_name = 'jobList_Pledge/registration_form.html';
    
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
                    return redirect('jobList_Pledge:index');
        return render(request, self.template_name, {'form': form});
                    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    