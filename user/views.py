from django.contrib.auth.decorators import login_required;
from django.shortcuts import render, get_object_or_404, redirect;
from django.contrib.auth.models import User;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from django.db.models import Q;
from django.contrib.auth import authenticate, login, logout;
from . import forms;
from .models import UserProfile;
from job.models import Job;
from datetime import datetime;
from random import randint;
import logging;

def sign_in(request):
    userForm = forms.UserForm(request.POST or None);
    newUserForm = forms.NewUserForm(request.POST or None);
    if (request.user.is_authenticated()):
        return redirect('job:home');
    else: 
        if (request.method == 'POST'):
            if ('sign-in' in request.POST):
                if (userForm.is_valid()):
                    email = userForm.cleaned_data['email'];
                    if (email != "" and User.objects.filter(email=email).exists()):
                        user = authenticate(username=User.objects.get(email=email).username, password=userForm.cleaned_data['password']);
                        if (user is not None):
                            if (not user.is_active):
                                user.is_active = True;
                            login(request, user);
                            return redirect('job:home');
            elif ('sign-up' in request.POST):
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
                        login(request, user);
                        return redirect('user:detail', user.username);
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
        
def getUsersFromQuery(search, num_searches):
    users = User.objects.all();
    for word in search.split():
        users = users.filter(Q(first_name__istartswith=word) | Q(last_name__istartswith=word));
    start = (50 * num_searches);
    end = start + 50;
    users = users[start:end];
    return users;
    
def see_more_users(request):
    if (request.is_ajax()):
        search = request.GET['search'];
        num_searches = request.GET['num_searches'];
        users = getUsersFromQuery(search, num_searches);
        users = serializers.serialize("json", users);
        return HttpResponse(users, content_type="application/json");
    else:
        return Http404();
    
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
        return redirect('user:detail', username=username);
    context = {
        'detail_user' : user,
        'current_jobusers' : user.jobuser_set.filter(job__is_finished=False),
        'finished_jobusers' : user.jobuser_set.filter(job__is_finished=True),
    }
    return render(request, 'user/detail.html', context);
    
@login_required
def account(request):
    change_name_form = None;
    if (request.method == "POST"):
        if ('change-name' in request.POST):
            form = forms.ChangeNameForm(request.POST);
            if (form.is_valid()):
                request.user.first_name = form.cleaned_data['first_name'];
                request.user.last_name = form.cleaned_data['last_name'];
                request.user.userprofile.last_time_name_was_changed = datetime.now();
                request.user.save();
                request.user.userprofile.save();
        elif ('change-email' in request.POST):
            form = forms.ChangeEmailForm(request.POST);
            if (form.is_valid()):
                request.user.email = form.cleaned_data['email'];
                request.user.save();
        elif ('change-password' in request.POST):
            form = forms.ChangePasswordForm(request.POST, user=request.user);
            if (form.is_valid()):
                request.user.set_password(form.cleaned_data['new_password']);
                request.user.save();
        elif ('delete-account' in request.POST):
            form = forms.DeactivateAccountForm(request.POST);
            if (form.is_valid()):
                request.user.is_active = False;
                sign_out(request);
        return redirect('user:account');
    if ((datetime.now() - request.user.userprofile.last_time_name_was_changed.replace(tzinfo=None)).days >= 180):
        change_name_form = forms.ChangeNameForm(initial = {'first_name' : request.user.first_name, 'last_name' : request.user.last_name});
    context = {
        'change_name_form' : change_name_form,
        'change_email_form' : forms.ChangeEmailForm(initial = {'email' : request.user.email}),
        'change_password_form' : forms.ChangePasswordForm(),
        'deactivate_account_form' : forms.DeactivateAccountForm(),
    }
    return render(request, 'user/account.html', context);
    
    
    
    