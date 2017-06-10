from django.contrib.auth.decorators import login_required;
from django.shortcuts import render, get_object_or_404;
from django.http import HttpResponse, Http404;
from django.contrib.auth.models import User;
from .models import JobUser, ImageUpload;
from job.models import Job;

@login_required
def post_update(request, workjob_id):
    jobuser = get_object_or_404(JobUser, pk=workjob_id);
    if (request.method == 'POST'):
        form = NewWorkJobUpdate(request.POST, request.FILES);
        if (form.is_valid()):
            title = form.cleaned_data['title'];
            description = form.cleaned_data['description'];
            update = Update(jobuser=jobuser, title=title, description=description);
            update.save();
            for image in request.FILES.getlist('images'):
                image=ImageUpload(image=image, update=update);
                image.save();
    if (jobuser.user == request.user):
        context = {
            'jobuser' : jobuser,
            'update_form' : NewWorkJobUpdate(),
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
    
@login_required    
def view_updates(request):
    return render(request, 'jobuser/view_updates.html');
    
def createUpdate(user, job, description):
    return None;
    
    
    
    
    
    
    
    
    
