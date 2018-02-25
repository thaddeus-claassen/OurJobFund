from django.contrib.auth.decorators import login_required;
from rest_framework.renderers import JSONRenderer;
from django.utils.decorators import method_decorator;
from django.views.generic import TemplateView;
from notification.models import Notification;
from annoying.functions import get_object_or_None;
from django.utils.html import escape;
from django.shortcuts import render, get_object_or_404, redirect;
from django.db.models import Q, F;
from jobuser.models import JobUser;
from update.models import Update;
from .serializers import JobSerializer;
from filter.forms import PledgeFilterForm, WorkerFilterForm;
from django.http import HttpResponse, Http404;
from django.core import serializers;
from pay.models import Pay;
from .models import Job, Tag, User, Image;
from .forms import NewJobForm;
from random import randint;
import json, re, math;

def home(request):
    return render(request, 'job/home.html');
    
def get_jobs(request):
    if (request.is_ajax()):
        jobs = findJobs(request);
        if (jobs == "Invalid Search"):
            return HttpResponse(jobs, content_type="application/json");
        else:
            jobs = jobs[0:50];
            serializer = JobSerializer(jobs, many=True, context={'user' : request.user});
            json = JSONRenderer().render(serializer.data);
            return HttpResponse(json, content_type="application/json");
    else:
        return Http404();

def add_jobs(request):
    if (request.is_ajax()):
        numSearches =  int(request.GET['numSearches']);
        jobs = findJobs(request);
        if (jobs == "Invalid Search"):
            return HttpResponse(jobs, content_type="application/json");
        else:
            jobs = jobs[50 * numSearches:50 * (numSearches + 1)];
            serializer = JobSerializer(jobs, many=True, context={'user' : request.user});
            json = JSONRenderer().render(serializer.data);
            return HttpResponse(json, content_type="application/json");
    else:
        return Http404();
        
def sort_jobs(request):
    if (request.is_ajax()):
        numSearches =  int(request.GET['numSearches']);
        jobs = findJobs(request);
        if (jobs == "Invalid Search"):
            return HttpResponse(jobs, content_type="application/json");
        else:
            jobs = jobs[0:50 * numSearches];
            serializer = JobSerializer(jobs, many=True, context={'user' : request.user});
            json = JSONRenderer().render(serializer.data);
            return HttpResponse(json, content_type="application/json");
    else:
        return Http404();
        
def get_total_jobs(request):
    if (request.is_ajax()):
        total = {};
        jobs = findJobs(request);
        if (jobs == "Invalid Search"):
            total = "";
        else:
            total['total'] = len(jobs);
        return HttpResponse(json.dumps(total), content_type="application/json");
    else:
        return Http404();
        
def findJobs(request):
    type = request.GET['type'];
    search = request.GET['search'];
    if (search == ""):
        jobs = Job.objects.all();
    else:
        if (type == 'basic'):
            if (re.match(r'^[A-Za-z0-9\s_]+$', search)):
                jobs = get_jobs_from_custom_search(search);
                jobs = Job.objects.all();
                for word in search.split(" "):
                    jobs = jobs.filter(Q(name__icontains=word) | Q(tag__tag__icontains=word));
            else:
                return "Invalid Search";
        else:
            if (re.match(r'^[A-Za-z0-9\s_&\|\(\)~]+$', search)):
                jobs = get_jobs_from_custom_search(search);
            else:
                return "Invalid Search";
    jobs = jobs.distinct();
    sort_array = request.GET['sort'].split(" ");
    latitude_in_degrees_as_string = request.GET['latitude'];
    longitude_in_degrees_as_string = request.GET['longitude'];
    radius_in_miles_as_string = request.GET['radius'];
    if (latitude_in_degrees_as_string != "" and longitude_in_degrees_as_string != "" and radius_in_miles_as_string != ""):
        jobs = findJobsByRadius(jobs, float(latitude_in_degrees_as_string), float(longitude_in_degrees_as_string), float(radius_in_miles_as_string));
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
    
def get_jobs_from_custom_search(tags):
        return eval(re.sub(r'([a-zA-Z0-9_]+)', "Job.objects.filter(tag__tag__iexact='" + r'\1' + "')", tags));
    
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
        distance = RADIUS_OF_EARTH_IN_MILES * math.acos(math.sin(latitude_in_radians) * math.sin(lat) + math.cos(latitude_in_radians) * math.cos(lat) * math.cos(math.fabs(longitude_in_radians - lon))); #This is called the Spherical Law of Cosines and it is used to calculate distances on a sphere. (Note: Earth is not a sphere, thus this will have a margin of error, but it is small. Quicker computation speed compensates)
        if (distance > radius_in_miles):
            jobs = jobs.exclude(id=job.id);
    return jobs;
    
@login_required
def save_filter(request):
    if (request.is_ajax()):
        changed_filter = request.POST['filter'];
        filter = changed_filter.split("-")[0];
        row = changed_filter.split("-")[1];
        value = request.POST['value'];
        if (value == ''):
            value = 0;
        exec("request.user." + str(filter) + "filter." + row + " = " + str(value));
        exec("request.user." + str(filter) + "filter.save()");
        return HttpResponse("");
    else:
        return Http404();
        
@login_required
def save_search_type(request):
    if (request.is_ajax()):
        request.user.profile.basic_search = (request.POST['isBasic'] == 'true');
        request.user.profile.save();
        return HttpResponse("");
    else:
        return Http404();
        
@login_required
def save_hide_location(request):
    if (request.is_ajax()):
        request.user.profile.hide_location = (request.POST['isHidden'] == 'true');
        request.user.profile.save();
        return HttpResponse("");
    else:
        return Http404();

    
class DetailView(TemplateView):
    template_name = 'job/detail.html';
    
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        if (request.user.is_authenticated()):
            if (Notification.objects.filter(user=request.user, job=job).exists()): 
                Notification.objects.get(user=request.user, job=job).delete();
        return render(request, self.template_name, self.get_context_data(request, job=job))
    
    def get_context_data(self, request, **kwargs):
        job = kwargs['job'];
        context = {
            'job': job,
            'updates' : Update.objects.filter(jobuser__job=job).order_by('-date'),
            'pledges' : JobUser.objects.filter(Q(job=job) & (Q(pledged__gt=0) | Q(paid__gt=0))),
            'workers' : JobUser.objects.filter(job=job).exclude(work_status=''),
        }
        if (request.user.is_authenticated()):
            serializer = JobSerializer(Job.objects.filter(pk=job.pk), many=True, context={'user' : request.user});
            jobuser = get_object_or_None(JobUser, user=request.user, job=job);
            payment_verification = False;
            if (jobuser):
                for pay in jobuser.receiver_jobuser.all():
                    if (pay.type == 'Other' and not pay.verified):
                        payment_verification = True;
            context['jobuser'] = jobuser;
            context['payment_verification'] = payment_verification; 
        return context;

@login_required
def detail_sort(request, job_random_string):
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

class CreateView(TemplateView):
    template_name = 'job/create.html'; 
    form = NewJobForm;

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(form=self.form));
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST);
        if (form.is_valid()):
            name = form.cleaned_data['name'];
            latitude = form.cleaned_data['latitude'];
            longitude = form.cleaned_data['longitude'];
            location = form.cleaned_data['location'];
            tags = form.cleaned_data['tags'];
            description = form.cleaned_data['description'];
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
            jobuser = JobUser(user=request.user, job=job);
            jobuser.save();
            return redirect(job);
        return render(request, self.template_name, self.get_context_data(form=form));
        
    def get_context_data(self, **kwargs):
        context = {
            'form' : kwargs['form'],
        }
        return context
    
def createRandomString():
    random_string = '';
    available_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
    for i in range(50):
        index = randint(0, len(available_chars)-1);
        random_char = available_chars[index];
        random_string = random_string + random_char;
    if (Job.objects.filter(random_string=random_string).exists()):
        random_string = createRandomString();
    return random_string;
                   
                    
                    
    