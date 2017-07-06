from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect;
from django.contrib.auth.models import User;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from django.db.models import Q;
from django.contrib.auth import authenticate, login, logout;
from .forms import UserForm, NewUserForm, DescriptionForm;
from .models import UserProfile;
from job.models import Job;
from datetime import datetime;
from random import randint;

def sign_in(request):
    userForm = UserForm();
    newUserForm = NewUserForm();
    if (request.user.is_authenticated()):
        return redirect('job/home');
    else: 
        if (request.method == 'POST'):
            if ('sign-in' in request.POST):
                userForm = UserForm(request.POST);
                if (userForm.is_valid()):
                    email = userForm.cleaned_data['email'];
                    if (email != ""):
                        user = authenticate(username=User.objects.get(email=email).username, password=userForm.cleaned_data['password']);
                        if (user is not None):
                            if (user.is_active):
                                login(request, user);
                                return redirect('job:home');
            elif ('sign-up' in request.POST):
                newUserForm = NewUserForm(request.POST);
                if (newUserForm.is_valid()):
                    user = newUserForm.save(commit=False);
                    first_name = newUserForm.cleaned_data['first_name'];
                    last_name = newUserForm.cleaned_data['last_name'];
                    user.first_name = first_name;
                    user.last_name = last_name;
                    user.email = newUserForm.cleaned_data['email'];
                    password = newUserForm.cleaned_data['password'];
                    user.set_password(password);
                    user.username = createNewUsername(first_name, last_name);
                    user.save();
                    UserProfile(user=user).save();
                    user = authenticate(username=user.username, password=password);
                    if (user is not None):
                        if (user.is_active):
                            login(request, user);
                            return redirect('job:home');
    context = {
        'new_user_form' : newUserForm, 
        'existing_user_form' : userForm,
    }
    return render(request, 'user/signup.html', context);
        
def check_email_is_unused(request):
    emailIsUnused = True;
    if (request.is_ajax()):
        emailIsUnused = not User.objects.filter(email=request.GET['email']).exists();
    return emailIsUnused;
    
def createNewUsername(first_name, last_name):
    combinedNames = first_name + last_name;
    lastDigit = 1;
    username = combinedNames + str(lastDigit);
    while (User.objects.filter(username=username).exists()):
       lastDigit = lastDigit + 1;
       username = combinedNames + str(lastDigit);
    return username;
        

@login_required        
def sign_out(request):
    logout(request);
    return redirect('user:sign_in');

@login_required    
def search_users(request):
    search = request.GET['search-users'];
    context = {
        'users' : getUsersFromQuery(search, 0),
        'search' : search,
        'total' : getTotalNumberOfUsersFromQuery(search),
    };
    return render(request, 'user/users.html', context);

def see_more_users(request):
    if (request.is_ajax()):
        search = request.GET['search'];
        num_searches = request.GET['num_searches'];
        users = getUsersFromQuery(search, num_searches);
        users = serializers.serialize("json", users);
        return HttpResponse(users, content_type="application/json");
    else:
        return Http404();
        
def getUsersFromQuery(search, num_searches):
    users = User.objects.all();
    for word in search.split():
        users = users.filter(Q(first_name__startswith=word) | Q(last_name__startswith=word));
    start = (50 * num_searches);
    end = start + 50;
    users = users[start:end];
    return users;
    
def getTotalNumberOfUsersFromQuery(search):
    users = User.objects.all();
    for word in search.split():
        users = users.filter(Q(first_name__startswith=word) | Q(last_name__startswith=word));
    return users.count();
         
@login_required    
def detail(request, username):
    user = get_object_or_404(User, username=username);
    if (request.method == 'POST'):
        request.user.userprofile.description = request.POST.get('description');
        request.user.userprofile.save();
    context = {
        'detail_user' : user,
        'current_jobusers' : user.jobuser_set.filter(job__is_finished=False),
        'finished_jobusers' : user.jobuser_set.filter(job__is_finished=True),
    }
    return render(request, 'user/detail.html', context);
    
    
    
    