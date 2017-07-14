from django.contrib.auth.decorators import login_required;
from django.shortcuts import render, get_object_or_404, redirect;
from .models import Job, Tag, User;
from user.models import Notification;
from django.db.models import Q;
from jobuser.models import JobUser, Pledge, Pay, Work, Finish, Update;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from django.contrib.auth import authenticate, login, logout;
from .forms import NewJobForm;
import json, re, math;
from random import randint;
from ourjobfund.settings import STRIPE_API_KEY;
import stripe;

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
        total['total'] = len(jobs)
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
        jobs = jobs.order_by('creation_date');
        if (sort_array[1] == 'descending'):
            jobs = jobs[::-1];
    elif (sort_array[0] == 'pledged'):
        jobs = jobs.order_by('money_pledged');
        if (sort_array[1] == 'descending'):
            jobs = jobs[::-1];
    elif (sort_array[0] == 'workers'):
        jobs = jobs.order_by('num_workers');
        if (sort_array[1] == 'descending'):
            jobs = jobs[::-1];
    else:
        jobs = jobs.extra(select={'case_insensitive_name': 'lower(name)'}).order_by('case_insensitive_name');
        if (sort_array[1] == 'descending'):
            jobs = jobs[::-1];
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
        if (distance > radius_in_miles):
            print("Excluded Job: " + job.name);
            jobs = jobs.exclude(id=job.id);
    return jobs;

@login_required    
def detail(request, job_random_string):
    job = get_object_or_404(Job, random_string=job_random_string);
    if (request.method == "POST"):
        print("Got into POST");
        jobuser = JobUser.objects.filter(user=request.user, job=job).first();
        print(request.POST);
        if (not jobuser):
            jobuser = JobUser(user=request.user, job=job);
            jobuser.save();
        if ('pledge_money_to_job' in request.POST):
            amount_pledged = float(request.POST.get('pledge_money_to_job'));
            if (amount_pledged >= 0.5):
                pledge = Pledge(jobuser=jobuser, amount=amount_pledged);
                pledge.save();
                jobuser.amount_pledged = jobuser.amount_pledged + amount_pledged;
        elif ('work_on_job' in request.POST):
            work = Work(jobuser=jobuser);
            work.save();
        elif ('finish_job' in request.POST):
            finish = Finish(jobuser=jobuser);
            finish.save();
        elif ('stripeToken' in request.POST):
            print("stripeToken is in request.POST");
            receiver_username = request.POST['pay_to'];
            receiver = None;
            if (User.objects.filter(username=receiver_username).exists()):
                receiver = User.objects.get(username=receiver_username);
            else:
                stripe.api_key = STRIPE_API_KEY;
                token = request.POST['stripeToken'];
                amount_paying = float(request.POST['pay_amount']);
                receiver_amount = amount_paying - (.05 * amount_paying);
                charge = stripe.Charge.create(
                    amount = amount_paying,
                    currency = "usd",
                    source = token,
                    destination = {
                        amount : receiver_amount,
                        account : jobuser.user.userprofile.stripe_account_id,
                    },
                );
                charge = stripe.Charge.create(
                    amount = amount_paying - receiver_amount,
                    currency = "usd",
                    source = token,
                );
                origJobuser = JobUser.objects.get(user=request.user, job=jobuser.job);
                payment = Pay(jobuser=origJobuser, receiver=jobuser.user, amount=plan.amount);
                origJobuser.amount_paid = origJobuser.amount_paid + plan.amount;
        return redirect('job:detail', job_random_string=job_random_string);
    pledges = Pledge.objects.filter(jobuser__job=job);
    total_pledged = 0;
    for pledge in pledges:
        total_pledged = total_pledged + pledge.amount;
    total_paid = 0;
    for pledge in pledges:
        for payment in pledge.jobuser.pay_set.all():
            total_paid = total_paid + payment;
    workers = Work.objects.filter(jobuser__job=job);
    total_working = workers.count() - Finish.objects.filter(jobuser__job=job).count();
    jobuser = None;
    if (JobUser.objects.filter(user=request.user, job=job).exists()):
        jobuser = request.user.jobuser_set.all().get(job=job);
    if (Notification.objects.filter(user=request.user, job=job).exists()): 
        Notification.objects.get(user=request.user, job=job).delete();
    updates = Update.objects.filter(jobuser__job=job);
    updates_last_name = updates.extra(select={'case_insensitive_last_name': 'lower(title)'}).order_by('case_insensitive_last_name');
    updates_date = updates.order_by('-date');
    updates_title = updates.extra(select={'case_insensitive_title' : 'lower(title)'}).order_by('case_insensitive_title');
    context = {                                                                     
        'job': job,
        'pledges' : pledges,
        'total_pledged' : total_pledged,
        'total_paid' : total_paid,
        'workers' : workers,
        'total_working' : total_working,
        'jobuser' : jobuser,
        'updates_last_name' : updates_last_name,
        'updates_date' : updates_date,
        'updates_title' : updates_title,
    }
    return render(request, 'job/detail.html', context);
    
@login_required
def pledge_money_to_job(request, job_random_string):
    string = "";
    if (request.method == 'POST'):
        job = get_object_or_404(Job, random_string=job_random_string);
        if (not job.pledgejob_set.filter(pledger=request.user).exists()):
            amount_pledged = float(request.POST['amount_pledged']);
            PledgeJob(pledger=request.user, job=job, amount_pledged=amount_pledged).save();
            job.money_pledged = job.money_pledged + amount_pledged;
            job.save();
            string += request.user.username + " " + amount_pledged; 
    return HttpResponse(string);
    
@login_required
def work_on_job(request, job_random_string):
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
                   
                    
                    
    