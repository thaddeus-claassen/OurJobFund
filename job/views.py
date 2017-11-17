from django.contrib.auth.decorators import login_required;
from django.utils.decorators import method_decorator;
from django.shortcuts import render, get_object_or_404, redirect;
from django.views.generic import TemplateView;
from annoying.functions import get_object_or_None;
from .models import Job, Tag, User, Image;
from .serializers import JobSerializer;
from notification.models import Notification;
from django.db.models import Q, F;
from jobuser.models import JobUser, Pledge, Pay, Work, Finish;
from update.models import Update;
from update.views import create_update_by_finishing, create_update_by_paying, create_update_by_unfinishing;
from django.http import HttpResponse, Http404;
from django.core import serializers;
from rest_framework.renderers import JSONRenderer;
from filter.forms import PledgeFilterForm, WorkerFilterForm;
from .forms import NewJobForm;
import json, re, math;
from random import randint;
from jobuser.forms import PledgeForm;
from ourjobfund.settings import STRIPE_TEST_SECRET_KEY, STATIC_ROOT;
import stripe;

def redirect_to_home(request):
    return redirect('job:home');

def home(request):
    context = None;
    if (request.user.is_authenticated()):
        context = {
            'worker_filter_form' : WorkerFilterForm(instance=request.user.workerfilter),
            'pledge_filter_form' : PledgeFilterForm(instance=request.user.pledgefilter),
        };
    return render(request, 'job/home.html', context);

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
        return redirect(job);
    else:
        return Http404();
    
def get_jobs(request):
    if (request.is_ajax()):
        jobs = findJobs(request);
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
        jobs = jobs[0:50 * numSearches];
        serializer = JobSerializer(jobs, many=True, context={'user' : request.user});
        json = JSONRenderer().render(serializer.data);
        return HttpResponse(json, content_type="application/json");
    else:
        return Http404();
        
def get_total_jobs(request):
    if (request.is_ajax()):
        jobs = findJobs(request);
        total = {};
        total['total'] = len(jobs)
        return HttpResponse(json.dumps(total), content_type="application/json");
    else:
        return Http404();
        
def findJobs(request):
    search_type = request.GET['search_type'];
    search = request.GET['search'];
    if (search_type == 'basic'):
        jobs = Job.objects.all();
        for word in search.split(" "):
            jobs = jobs.filter(Q(name__contains=word) | Q(tag__tag__contains=word));
    elif (search_type == "custom"):
        jobs = get_jobs_from_custom_search(search);
    jobs = jobs.distinct();
    sort_array = request.GET['sort'].split(" ");
    latitude_in_degrees_as_string = request.GET['latitude'];
    longitude_in_degrees_as_string = request.GET['longitude'];
    radius_in_miles_as_string = request.GET['radius'];
    print("Radius: " + str(radius_in_miles_as_string));
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
    return eval("Job.objects.filter(" + re.sub(r'([a-zA-Z0-9]+)', "Q(tag__tag__iexact='" + r'\1' + "')", tags) + ")");
    
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
    
class DetailView(TemplateView):
    template_name = 'job/detail.html';
    form = PledgeForm;
    
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        if (request.user.is_authenticated()):
            if (Notification.objects.filter(user=request.user, job=job).exists()): 
                Notification.objects.get(user=request.user, job=job).delete();
        return render(request, self.template_name, self.get_context_data(request, job=job))
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, random_string=kwargs['job_random_string']);
        jobuser = get_object_or_None(JobUser, job=job, user=request.user);
        if (not jobuser):
            jobuser = JobUser(user=request.user, job=job);
            jobuser.save();
        if ('pledge' in request.POST):
            self.pledge(self.form(request.POST), job, jobuser);
        elif ('work' in request.POST):
            self.work(job, jobuser);
        elif ('finish' in request.POST):
            self.finish(job, jobuser);
        elif ('unfinish' in request.POST):
            self.unfinish(job, jobuser);
        elif ('stripeToken' in request.POST):
            self.pay(request, job, jobuser);
            return redirect('job:confirmation', job_random_string=job.random_string);
        return redirect(job);
    
    def get_context_data(self, request, **kwargs):
        job = kwargs['job'];
        context = {                                                                     
            'job': job,
            'pledges' : Pledge.objects.filter(jobuser__job=job),
            'workers' : Work.objects.filter(Q(jobuser__job=job) & Q(date__exact=F('jobuser__oldest_work_date'))).order_by('-date'),
            
            'updates' : Update.objects.filter(jobuser__job=job).order_by('-date'),
        }
        if (request.user.is_authenticated()):
            context['jobuser'] = get_object_or_None(JobUser, user=request.user, job=job);
            context['user_has_stripe_account'] = (request.user.userprofile.stripe_account_id != None) and (request.user.userprofile.stripe_account_id != '');
            context['pledge_form'] = self.form;
        return context;
        
    def pledge(self, form, job, jobuser):
        if (form.is_valid()):
            amount_pledged = form.cleaned_data['amount'];
            pledge = Pledge(jobuser=jobuser, amount=amount_pledged);
            pledge.save();
            jobuser.amount_pledged = jobuser.amount_pledged + amount_pledged;
            jobuser.save();
            job.pledged = job.pledged + jobuser.amount_pledged;
            job.save();
            
    def work(self, job, jobuser):
        work = Work(jobuser=jobuser);
        work.save();
        jobuser.oldest_work_date = work.date;
        jobuser.save();
        job.workers = job.workers + 1;
        job.save();
            
    def finish(self, job, jobuser):
        finish = Finish(jobuser=jobuser);
        finish.save();
        job.finished = job.finished + 1;
        job.save();
        jobuser.newest_finish_date = finish.date;
        jobuser.save();
        create_update_by_finishing(finish);
        
    def unfinish(self, job, jobuser):
        unfinish = Work(jobuser=jobuser);
        unfinish.save();
        job.finished = job.finished - 1;
        job.save();
        create_update_by_unfinishing(unfinish);
    
    def pay(self, request, job, jobuser):
        receiver_username = request.POST['pay_to'];
        stripe.api_key = STRIPE_TEST_SECRET_KEY;
        token = request.POST['stripeToken'];
        amount_paying = int(request.POST['pay_amount']) * 100;
        charge = stripe.Charge.create(
            amount = amount_paying,
            currency = "usd",
            description = "Does this charge work?",
            source = token,
        );
        payment = Pay(jobuser=jobuser, receiver=jobuser.user, amount=float(amount_paying));
        payment.save();
        jobuser.amount_paid = jobuser.amount_paid + amount_paying;
        jobuser.save();
        receiver_jobuser = JobUser.objects.get(user=User.objects.get(username=receiver_username), job=job);
        receiver_jobuser.amount_received = receiver_jobuser.amount_received + amount_paying;
        receiver_jobuser.save();
        job.paid = job.paid + amount_paying;
        job.save();
        create_update_by_paying(payment);
            
@login_required
def payment_confirmation(request, job_random_string):
    job = get_object_or_404(Job, random_string = job_random_string);
    context = {
        'job' : job,
    }
    return render(request, 'job/confirmation.html', context);

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
        index = randint(0, 61);
        random_char = available_chars[index];
        random_string = random_string + random_char;
    if (Job.objects.filter(random_string=random_string).exists()):
        random_string = createRandomString();
    return random_string;
                   
                    
                    
    