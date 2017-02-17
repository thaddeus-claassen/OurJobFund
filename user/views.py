from django.shortcuts import render, get_object_or_404, redirect;
from django.contrib.auth.models import User;
from django.views.generic import View;
from django.http import HttpResponse;
from django.contrib.auth import authenticate, login, logout;
from .forms import UserForm, NewUserForm, NewWorkJobUpdate;
from .models import UserProfile, UserMessage, WorkJob, WorkJobUpdate, ImageUpload;
from job.models import Job, UserLogic, UserPledgeFilter, UserWorkerFilter;
from job.views import copy_pledge_filter_job, copy_worker_filter_job;

def create_user(request):
    if (request.method == 'POST'):
        newUserForm = NewUserForm(request.POST);
        if (newUserForm.is_valid()):
            username = newUserForm.cleaned_data['username'];
            email = newUserForm.cleaned_data['email'];
            password = newUserForm.cleaned_data['password'];
            user = User(username=username, email=email);
            user.set_password(password);
            user.save();
            user = authenticate(username=username, password=password);
            UserProfile(user=user).save();
            UserLogic(user=user).save();
            UserPledgeFilter(user=user).save();
            UserWorkerFilter(user=user).save();
            if user is not None:
                if user.is_active:
                    login(request, user);
                    return render(request, 'user/new_user_just_created.html');
    context = {
        'form' : NewUserForm(), 
    }
    return render(request, 'user/create_user.html', context);            

def search_users(request):
    print("Got into search_users in user.views ");
    response = "";
    if (request.method == 'GET'):
        username = request.GET['username'];
        if (User.objects.filter(username=username).exists()):
            response = "user exists";
        else:
            response = "user does not exist";
    pritn('Final Response: ' + response);
    return HttpResponse(response);
    
def verify_username(request):
    usernameExists = None;
    if (request.method == 'GET'):
        username = request.GET['username'];
        if (User.objects.filter(username__iexact=username).exists()):
            usernameExists = 'true';
        else:
            usernameExists = 'false';
    return HttpResponse(usernameExists);

def detail(request, user_username):
    user = get_object_or_404(User, username=user_username);       
    context = {
        'id' : user.id,
        'username' : user_username,
        'email' : user.email,
        'description' : user.userprofile.description,
        'pledge_filter_is_public' :  user.userworkerfilter.is_public,
        'worker_filter_is_public' :  user.userpledgefilter.is_public,
    }
    return render(request, 'user/detail.html', context);
    
def save_description(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            request.user.userprofile.description = request.POST['description'];
            print(request.user.userprofile.description);
            request.user.userprofile.save();
    return HttpResponse('Done!');
    
def post_update(request, workjob_id):
    print('Got in post_update')
    workjob = get_object_or_404(WorkJob, pk=workjob_id);
    print('Workjob: ');
    print(workjob)
    if (request.user.is_authenticated()):
        print('User is authenticated')
        if (request.method == 'POST'):
            print('request.method is post')
            form = NewWorkJobUpdate(request.POST, request.FILES);
            print('Form retrieved');
            print(form);
            if (form.is_valid()):
                print('Form is valid')
                title = form.cleaned_data['title'];
                description = form.cleaned_data['description'];
                newUpdate = WorkJobUpdate(workjob=workjob, title=title, description=description).save();
                for image in request.FILES.getlist('images'):
                    newUpdate.imageupload_set.add(image=ImageUpload(image=image));
            else:
                print('Form is not valid');
        else:
            if (workjob.worker == request.user):
                context = {
                    'workjob' : workjob,
                    'update_form' : NewWorkJobUpdate(),
                }
                return render(request, 'user/post_update.html', context);
    return detail(request, workjob.job.pk);
   
def view_update(request, update_id):
    update = get_object_or_404(Update, update_id);
    context = {
        'update' : update,
    }
    return render(request, 'view_update.hmtl', context);
    
def send_message(request):
    response = "Failure";
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            sender = request.user;
            receiver = User.objects.get(username=request.POST['receiver']);
            message = request.POST['message'];
            UserMessage(sender=sender, receiver=receiver, message=message).save();
            response = "Success";
    return HttpResponse(response);
    
def messages(request):
    if (request.user.is_authenticated()):
        return render(request, 'user/messages.html', {});
    return Http404();
            
def message(request, message_id):
    if (request.user.is_authenticated()):
        if (request.user.receivers.filter(pk=message_id).exists()):
            context = {
                'message' : request.user.get(pk=message_id),
            }
            return render(request, 'user/message.html', context);
    return Http404();
    
def change_public_pledge_filter(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            request.user.userworkerfilter.is_public = not request.user.userworkerfilter.is_public;
            request.user.userworkerfilter.save();
    return HttpResponse("Finished!");
    
def change_public_worker_filter(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            request.user.userpledgefilter.is_public = not request.user.userpledgefilter.is_public;
            request.user.userpledgefilter.save();
    return HttpResponse("Finished!");
    
def copy_pledge_filter(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated):
            otherUser = get_object_or_404(User, pk=request.POST['user_id']);
            copy_pledge_filter_job(request.user, otherUser);
    return HttpResponse('Finished!');
    
def copy_worker_filter(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated):
            otherUser = get_object_or_404(User, pk=request.POST['user_id']);
            copy_worker_filter_job(request.user, otherUser);
    return HttpResponse('Finished!');
        
    

        