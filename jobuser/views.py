from django.contrib.auth.decorators import login_required;
from django.shortcuts import render, get_object_or_404, redirect;
from django.http import HttpResponse, Http404;
from django.contrib.auth.models import User;
from .models import JobUser, Update, ImageUpload, Pay;
from user.models import Notification;
from job.models import Job;
from .forms import UpdateForm;

@login_required
def post_update(request, jobuser_id):
    jobuser = get_object_or_404(JobUser, pk=jobuser_id);
    if (request.method == 'POST'):
        form = UpdateForm(request.POST);
        if (form.is_valid()):
            title = form.cleaned_data['title'];
            description = form.cleaned_data['description'];
            update = Update(jobuser=jobuser, title=title, description=description);
            update.save();
            for image in request.FILES.getlist('images'):
                image=ImageUpload(image=image, update=update);
                image.save();
            sendNotifications(update);
            return redirect('job:detail', job_random_string=jobuser.job.random_string);
    if (jobuser.user == request.user):
        context = {
            'jobuser' : jobuser,
            'form' : UpdateForm(),
        }
        return render(request, 'jobuser/post_update.html', context);
    return redirect('/job/' + jobuser.job.random_string);
    
@login_required    
def view_update(request, update_id):
    update = get_object_or_404(Update, pk=update_id);
    context = {
        'user_is_working_on_job' : WorkJob.objects.filter(job=update.job, worker=request.user).exists(), 
        'update' : update,
    }
    return render(request, 'jobuser/view_update.html', context);
    
def sendNotifications(update):
    users = User.objects.filter(jobuser__job=update.jobuser.job).exclude(email=update.jobuser.user.email);
    for user in users:
        if not user.notification_set.filter(job=update.jobuser.job).exists():
            notification = Notification(user=user, job=update.jobuser.job);
            notification.save();
            
    
    
    
    
    
    
    
    
    
    
