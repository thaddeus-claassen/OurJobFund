from django.contrib.auth.decorators import login_required;
from django.shortcuts import render, get_object_or_404, redirect;
from annoying.functions import get_object_or_None;
from .models import Job, Tag, User, Image;
from .serializers import JobSerializer;
from notification.models import Notification;
from django.db.models import Q, F;
from jobuser.models import JobUser, Pledge, Pay, Work, Finish;
from update.models import Update;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from rest_framework.renderers import JSONRenderer;
from filter.forms import PledgeFilterForm, WorkerFilterForm;
from .forms import NewJobForm;
import json, re, math;
from random import randint;
from jobuser.forms import PledgeForm;
from ourjobfund.settings import STRIPE_TEST_SECRET_KEY, STATIC_ROOT;
import stripe;

@login_required
def pledge(request):
    context = {
        'worker_filter_form' : WorkerFilterForm(instance=request.user.workerfilter),
    };
    return render(request, 'job/pledge.html', context);

@login_required
def work(request):
    context = {
        'pledge_filter_form' : PledgeFilterForm(instance=request.user.pledgefilter),
    };
    return render(request, 'job/work.html', context);

@login_required
def get_stripe_info(request):
    job_random_string = request.GET.get('state', None);
    if (job_random_string is not None):
        job = get_object_or_404(Job, random_string=job_random_string);
        code = request.GET.get('code', None);
        request.user.userprofile.stripe_account_id = code;
        request.user.userprofile.save();
        jobuser = get_object_or_None(JobUser, user=request.user, job=job);
        if (not jobuser):
            jobuser = JobUser(user=request.user, job=job);
            jobuser.save();
        work = Work(jobuser=jobuser);
        work.save();
        return redirect('job:detail', job.random_string);
    else:
        return Http404();
    
@login_required
def get_jobs(request):
    if (request.is_ajax()):
        jobs = findJobs(request);
        jobs = jobs[0:50];
        serializer = JobSerializer(jobs, many=True, context={'user' : request.user});
        json = JSONRenderer().render(serializer.data);
        return HttpResponse(json, content_type="application/json");
    else:
        return Http404();

@login_required
def add_jobs(request):
    if (request.is_ajax()):
        numSearches =  int(request.GET['numSearches']);
        jobs = findJobs(request);
        jobs = jobs[50 * numSearches:50 * (numSearches + 1)];
        serializer = JobSerializer(jobs, many=True, context={'user' : request.user});
        json = JSONRenderer().render(serializer.data);
        return HttpResponse(jobs, content_type="application/json");
    else:
        return Http404();

@login_required        
def sort_jobs(request):
    if (request.is_ajax()):
        numSearches =  int(request.GET['numSearches']);
        jobs = findJobs(request);
        jobs = jobs[0:50 * numSearches];
        serializer = JobSerializer(jobs, many=True, context={'user' : request.user});
        json = JSONRenderer().render(serializer.data);
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
    elif (sort_array[0] == 'pledged'):
        jobs = jobs.order_by('pledged');
    elif (sort_array[0] == 'workers'):
        jobs = jobs.order_by('workers');
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
            jobs = jobs.exclude(id=job.id);
    return jobs;

@login_required    
def detail(request, job_random_string):
    job = get_object_or_404(Job, random_string=job_random_string);
    pledgeForm = PledgeForm(request.POST or None);
    if (request.method == "POST"):
        jobuser = JobUser.objects.filter(user=request.user, job=job).first();
        if (not jobuser):
            jobuser = JobUser(user=request.user, job=job);
            jobuser.save();
        if ('pledge' in request.POST):
            if (pledgeForm.is_valid()):
                amount_pledged = pledgeForm.cleaned_data['amount'];
                pledge = Pledge(jobuser=jobuser, amount=amount_pledged);
                pledge.save();
                jobuser.amount_pledged = jobuser.amount_pledged + amount_pledged;
                jobuser.save();
                job.pledged = job.pledged + jobuser.amount_pledged;
                job.save();
        elif ('work' in request.POST):
            work = Work(jobuser=jobuser);
            work.save();
            job.workers = job.workers + 1;
            job.save();
            jobuser.newest_work_date = work.date;
            jobuser.save();
        elif ('finish' in request.POST):
            finish = Finish(jobuser=jobuser);
            finish.save();
            job.finished = job.finished + 1;
            job.save();
            jobuser.newest_finish_date = finish.date;
            jobuser.save()
        elif ('unfinish' in request.POST):
            unfinish = Work(jobuser=jobuser);
            unfinish.save();
            job.finished = job.finished - 1;
            job.save();
            jobuser.newest_work_date = unfinish.date;
            jobuser.save();
        elif ('stripeToken' in request.POST):
            receiver_username = request.POST['pay_to'];
            stripe.api_key = STRIPE_TEST_SECRET_KEY;
            token = request.POST['stripeToken'];
            amount_paying = int(request.POST['pay_amount']);
            try:
                charge = stripe.Charge.create(
                    amount = amount_paying,
                    currency = "usd",
                    source = token,
                    description = "Does this charge work?",
                    #destination = {
                        #    'account' : jobuser.user.userprofile.stripe_account_id,
                    #},
                );
                payment = Pay(jobuser=jobuser, receiver=jobuser.user, amount=float(amount_paying));
                payment.save();
                jobuser.amount_paid = jobuser.amount_paid + amount_paying;
                jobuser.save();
                job.paid = job.paid + amount_paying;
                job.save();
            except:
                return HttpResponse(stripe.Charge);
        return redirect('job:detail', job_random_string=job_random_string);
    workers = Work.objects.filter(Q(jobuser__job=job) & Q(date__exact=F('jobuser__newest_work_date'))).order_by('-date');
    total_finished = 0;
    for jobuser in JobUser.objects.filter(job=job):
        if (jobuser.work_set.all().count() == jobuser.finish_set.all().count()):
            total_finished = total_finished + 1;
    total_working = workers.count() - total_finished;
    if (Notification.objects.filter(user=request.user, job=job).exists()): 
        Notification.objects.get(user=request.user, job=job).delete();
    context = {                                                                     
        'job': job,
        'pledges' : Pledge.objects.filter(jobuser__job=job),
        'total_pledged' : int(job.pledged),
        'total_paid' : int(job.paid),
        'workers' : workers,
        'total_working' : total_working,
        'total_finished' : total_finished,
        'jobuser' : get_object_or_None(JobUser, user=request.user, job=job),
        'updates' : Update.objects.filter(jobuser__job=job).order_by('-date'),
        'user_has_stripe_account' : (request.user.userprofile.stripe_account_id != None) and (request.user.userprofile.stripe_account_id != ''),
        'pledge_form' : pledgeForm,
    }
    return render(request, 'job/detail.html', context);

@login_required
def detail_sort(request, job_random_string):
    rows = None;
    if (request.is_ajax()):
        job = get_object_or_404(Job, random_string=job_random_string);
        sort = request.GET.get('sort');
        descending_or_ascending = request.GET.get('descending_or_ascending');
        updates = Update.objects.filter(jobuser__job=job);
        if (sort == 'last_name'):
            rows = updates.extra(select={'case_insensitive_last_name': 'lower(title)'}).order_by('case_insensitive_last_name');
        elif (sort == 'date'):
            rows = updates.order_by('date');
        elif (sort == 'title'):
            rows = updates.extra(select={'case_insensitive_title' : 'lower(title)'}).order_by('case_insensitive_title');
        elif (sort == 'update-images'):
            rows = updates.extra(select={'image_count' : 'image_set.count()'}).order_by('image_count');
        if (descending_or_ascending == 'descending'):
            updates = updates[::-1];
        rows = serializers.serialize('json', rows);
        return HttpResponse(rows, content_type="application/json");
    else:
        return Http404();

@login_required
def create_job(request):
    newJobForm = NewJobForm(request.POST or None);
    if (request.method == 'POST'):
        if (newJobForm.is_valid()):
            name = newJobForm.cleaned_data['name'];
            latitude = newJobForm.cleaned_data['latitude'];
            longitude = newJobForm.cleaned_data['longitude'];
            location = newJobForm.cleaned_data['location'];
            tags = newJobForm.cleaned_data['tags'];
            description = newJobForm.cleaned_data['description'];
            job = Job(name=name, latitude=latitude, longitude=longitude, location=location, description=description, created_by=request.user, random_string=createRandomString());
            job.save();
            if (tags != ''):
                tagsArray = tags.split(" ");
                for tagString in tagsArray:
                    newTag = get_object_or_None(Tag, tag=tagString)
                    if (not newTag):
                        newTag = Tag(tag=tagString);
                        newTag.save();
                    job.tag_set.add(newTag);
            for image in request.FILES.getlist('image_set'):
                image = Image(image=image, job=job);
                image.save();
            return redirect('job:detail', job.random_string);
    context = {
        'form' : newJobForm, 
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
                   
                    
                    
    