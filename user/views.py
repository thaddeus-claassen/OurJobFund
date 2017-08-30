from django.contrib.auth.decorators import login_required;
from django.shortcuts import render, get_object_or_404, redirect;
from django.contrib.auth.models import User;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from django.db.models import Q, F;
from django.contrib.auth import authenticate, login, logout;
from . import forms;
from .models import UserProfile;
from job.models import Job;
from datetime import datetime;
from random import randint;
import logging;

def bagel(request):
    return HttpResponse("<html>Hi</html>");

def sign_in(request):
    if (request.user.is_authenticated()):
        return redirect('job:home');
    else: 
        userForm = forms.UserForm(request.POST or None);
        newUserForm = forms.NewUserForm(request.POST or None);
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
    infoForm = None;
    descriptionForm = None;
    print(request.user.userprofile.city);
    infoForm = forms.EditInfoForm(request.POST or None, initial={'city' : request.user.userprofile.city, 'state' : request.user.userprofile.state, 'occupation' : user.userprofile.occupation});
    descriptionForm = forms.EditDescriptionForm(request.POST or None, initial={'description' : user.userprofile.description});    
    if (request.method == "POST"):
        if (infoForm.has_changed()):
            if (infoForm.is_valid()):
                user.userprofile.city = infoForm.cleaned_data['city'];
                user.userprofile.state = infoForm.cleaned_data['state'];
                user.userprofile.occupation = infoForm.cleaned_data['occupation'];
                user.userprofile.save();
                return redirect('user:detail', username=request.user.username);
        if (descriptionForm.has_changed()):
            if (descriptionForm.is_valid()):
                user.userprofile.description = descriptionForm.cleaned_data['description'];
                user.userprofile.save();
                return redirect('user:detail', username=request.user.username);
    context = {
        'detail_user' : user,
        'info_form' : infoForm,
        'description_form' : descriptionForm,
        'current_jobusers' : user.jobuser_set.filter(Q(job__pledged=0) | Q(job__pledged__gt=F('job__paid'))),
        'finished_jobusers' : user.jobuser_set.filter(Q(job__pledged__gt=0) & Q(job__pledged__lte=F('job__paid'))),
    }
    return render(request, 'user/detail.html', context);
    
@login_required
def account(request):
    changeNameForm = None;
    changeEmailForm = forms.ChangeEmailForm(request.POST or None, initial = {'email' : request.user.email});
    changePasswordForm = forms.ChangePasswordForm(request.POST or None, user = request.user);
    deactivateAccountForm = forms.DeactivateAccountForm(request.POST or None, initial = {'is_active' : True});
    if ((datetime.now() - request.user.userprofile.last_time_name_was_changed.replace(tzinfo=None)).days >= 180):
        changeNameForm = forms.ChangeNameForm(request.POST, initial = {'first_name' : request.user.first_name, 'last_name' : request.user.last_name});
    if (request.method == "POST"):
        if (changeNameForm.has_changed()):
            if (changeNameForm.is_valid()):
                request.user.first_name = form.cleaned_data['first_name'];
                request.user.last_name = form.cleaned_data['last_name'];
                request.user.userprofile.last_time_name_was_changed = datetime.now();
                request.user.save();
                request.user.userprofile.save();
                return redirect('user:detail', username=request.user.username);
        if (changeEmailForm.has_changed()):
            if (form.is_valid()):
                request.user.email = form.cleaned_data['email'];
                request.user.save();
                return redirect('user:detail', username=request.user.username);
        if (changePasswordForm.has_changed()):
            if (form.is_valid()):
                request.user.set_password(form.cleaned_data['new_password']);
                request.user.save();
                return redirect('user:detail', username=request.user.username);
        if (deactivateAccountForm.has_changed()):
            if (form.is_valid()):
                request.user.is_active = False;
                sign_out(request);
    context = {
        'change_name_form' : changeNameForm,
        'change_email_form' : changeEmailForm,
        'change_password_form' : changePasswordForm,
        'deactivate_account_form' : deactivateAccountForm,
    }
    return render(request, 'user/account.html', context);
    
    
    
    