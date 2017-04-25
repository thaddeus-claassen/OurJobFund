from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect;
from django.contrib.auth.models import User;
from django.views.generic import View;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from django.db.models import Q;
from django.contrib.auth import authenticate, login, logout;
from .forms import UserForm, NewUserForm;
from jobuser.forms import NewWorkJobUpdate;
from .models import UserProfile, Messages, UserMessage;
from jobuser.models import WorkJob, ImageUpload, WorkJobUpdate;
from job.models import Job;
from datetime import datetime;
from random import randint;

def sign_in(request):
    if (request.user.is_authenticated()):
        return redirect('job/home');
    else: 
        if (request.method == 'POST'):
            userForm = UserForm(request.POST);
            newUserForm = NewUserForm(request.POST);
            if (userForm.is_valid()):
                email = userForm.cleaned_data['email'];
                password = userForm.cleaned_data['password'];
                user = authenticate(email=email, password=password);
                if (user is not None):
                    if (user.is_active):
                        login(request, user);
                        return redirect('job/home');
            elif (newUserForm.is_valid()):
                first_name = newUserForm.cleaned_data['first_name'];
                last_name = newUserForm.cleaned_data['last_name'];
                email = newUserForm.cleaned_data['email'];
                password = newUserForm.cleaned_data['password'];
                user = User(email=email);
                user.set_password(password);
                user.save();
                user = authenticate(email=email, password=password);
                random_string = create_user_random_string();
                UserProfile(user=user, random_string=random_string).save();
                if (user is not None):
                    if (user.is_active):
                        login(request, user);
                        return redirect('user/' + random_string);
        context = {
            'new_user_form' : NewUserForm(), 
            'existing_user_form' : UserForm(),
        }
        return render(request, 'user/create_user.html', context);
        
def sign_out(request):
    logout(request);
    return redirect('user:sign_in');

@login_required    
def search_users(request):
    if (request.is_ajax()):
        response = "";
        username = request.GET['username'];
        if (User.objects.filter(username__iexact=username).exists()):
            response = "user exists";
        else:
            response = "user does not exist";
        return HttpResponse(response);
    else:
        return Http404();

@login_required    
def detail(request, user_random_string):
    user = get_object_or_404(User, random_string=user_random_string);       
    context = {
        'id' : user.id,
        'username' : user_username,
        'email' : user.email,
        'description' : user.userprofile.description,
    }
    return render(request, 'user/detail.html', context);

@login_required    
def get_user_info(request):
    if (request.is_ajax()):
        data = {};
        user_id = request.GET['user_id'];
        user = get_object_or_404(User, pk=user_id);
        data['first_name'] = user.first_name;
        data['last_name'] = user.last_name;
        data['city'] = user.userprofile.city;
        data['state'] = user.userprofile.state;
        data['description'] = user.userprofile.description;
        return JsonResponse(data, safe=False);
    else:
        return Http404();

@login_required    
def save_description(request):
    if (request.is_ajax()):
        if (request.method == 'POST'):
            if (request.user.is_authenticated()):
                request.user.userprofile.description = request.POST['description'];
                request.user.userprofile.save();
        return HttpResponse('Done!');
    else:
        return Http404();
    

def create_user_random_string(request):
    random_string = '';
    available_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
    for i in range(20):
        index = randint(0, 61);
        random_char = available_chars[index];
        random_string = random_string + random_char;
    return random_string;
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
        