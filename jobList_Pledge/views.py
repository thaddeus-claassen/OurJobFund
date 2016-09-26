from django.shortcuts import render, render_to_response, get_object_or_404;
from .models import Job, Hashtag;
from django.http import JsonResponse, HttpResponse;
from django.core import serializers;
import json;



# This subroutine returns the JSON objects for the main job table in index.html
def job_table(jobs):
    return HttpResponse(                                        #Returns the HttpResponse as a JSON object for the main job table 
            jobs,                                               #   Names the object we want to send as JSON
            content_type="application/json",                    #   For some reason, we have to say this line. I guess so whatever reads this response knows its a JSON object
        );
  
# This gets the any jobs which match the name or id search in index.html
def search_jobs(request):    
    data = [];
    if (request.method == 'POST'):                               #if the request was a GET (I don't know why I'm supposed to do this, only the GET request from the search bar should calls method)
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
    
def apply_basic_hashtags(request):
    data = [];
    if (request.method == 'POST'):
        post_text = request.POST['hashtags'];
        if (post_text != ''):
            post_text = post_text.replace(" ", "");
            hashtagsArray = post_text.split(",");     
            data = Job.objects.all();
            for hashtagString in hashtagsArray :
                currHashtag = Hashtag.objects.get(hashtag__iexact=hashtagString);
                currJobs = currHashtag.jobs.all();
                data = data & currJobs;
    data = serializers.serialize("json", data);
    return job_table(data);
    
def ANDs_of_ORs(request):
    

    
def index(request):
    return render(request, 'jobList_Pledge/index.html');

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
