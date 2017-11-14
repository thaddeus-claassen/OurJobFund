from django.contrib.auth.decorators import login_required;
from django.utils.decorators import method_decorator;
from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect;
from annoying.functions import get_object_or_None;
from django.views.generic import TemplateView;
from django.contrib.auth.models import User;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from django.db.models import Q, F;
from django.contrib.auth import authenticate, login, logout;
from .forms import ChangePasswordForm, ChangeNameForm, ChangeEmailForm, LoginForm, NewUserForm, DeactivateAccountForm, DescriptionForm;
from .models import UserProfile, UserInfo;
from job.models import Job;
from datetime import datetime;
from random import randint;
import logging;

class LoginView(TemplateView):
   
    def get(self, request, *args, **kwargs):
        return redirect('user:sign_up');
    
    def post(self, request, *args, **kwargs):
        if ('sign-in' in request.POST):
            userForm = LoginForm(request.POST);
            if (userForm.is_valid()):
                email = userForm.cleaned_data['email'];
                if (email != "" and User.objects.filter(email=email).exists()):
                    user = authenticate(username=User.objects.get(email=email).username, password=userForm.cleaned_data['password']);
                    if (user is not None):
                        user.is_active = True;
                        login(request, user);
                        return redirect('job:home');
        return redirect('user:sign_up');

class SignUpView(TemplateView):
    template_name = 'user/signup.html';
    new_user_form = NewUserForm;
    
    def get(self, request, *args, **kwargs):
        if (request.user.is_authenticated()):
            return redirect('user:detail', username=request.user.username);
        else:
            return render(request, self.template_name, self.get_context_data(new_user_form=self.new_user_form));
    
    def post(self, request, *args, **kwargs):
        if (request.user.is_authenticated()):
            return redirect(request.user);
        form = self.new_user_form;
        if ('sign-up' in request.POST):
            form = form(request.POST);
            if (form.is_valid()):
                user = form.save(commit=False);
                user.email = form.cleaned_data['email'];
                user.username = form.cleaned_data['username'];
                password = form.cleaned_data['password'];
                user.set_password(password);
                user.save();
                user = authenticate(username=user.username, password=password);
                if (user is not None):
                    login(request, user);
                    return redirect(user);
        return render(request, self.template_name, self.get_context_data(new_user_form=form));
        
    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs);
        context['new_user_form'] = kwargs['new_user_form'];
        return context;

@login_required        
def sign_out(request):
    logout(request);
    return redirect('user:sign_up');

@login_required    
def search_users(request):
    search = request.GET['search-users'];
    context = {
        'users' : getUsersFromQuery(search, 0),
        'search' : search,
        'total' : getTotalNumberOfUsersFromQuery(search),
    };
    return render(request, 'user/search.html', context);
        
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
 
class DetailView(TemplateView):
    template_name = 'user/detail.html';
    descriptionForm = DescriptionForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username']);
        self.descriptionForm = self.descriptionForm(initial={'description' : user.userprofile.description});
        return render(request, self.template_name, self.get_context_data());
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if ('description_form' in request.POST):
            self.descriptionForm = self.descriptionForm(request.POST);
            if (self.descriptionForm.is_valid()):
                request.user.userprofile.description = self.descriptionForm.cleaned_data['description'];
                request.user.userprofile.save();
                return redirect(request.user);
        return render(request, self.template_name, self.get_context_data({'username' : kwargs['username']}));
        
    def get_context_data(self, *args, **kwargs):
        user = get_object_or_None(User, username=self.kwargs['username']);
        context = {
            'detail_user' : user,
            'description_form' : self.descriptionForm,
            'current_jobusers' : user.jobuser_set.filter(Q(job__pledged=0) | Q(job__pledged__gt=F('job__paid'))),
            'finished_jobusers' : user.jobuser_set.filter(Q(job__pledged__gt=0) & Q(job__pledged__lte=F('job__paid'))),
        }
        return context;
    
class AccountView(TemplateView):
    template_name = 'user/account.html';
    nameForm = None;
    emailForm = ChangeEmailForm;
    passwordForm = ChangePasswordForm;
    deactivateForm = DeactivateAccountForm;
    changeNameForm = ChangeNameForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if ((datetime.now() - request.user.userprofile.last_time_name_was_changed.replace(tzinfo=None)).days >= 180):
            self.nameForm = self.changeNameForm(initial = {'first_name' : request.user.first_name, 'last_name' : request.user.last_name});
        self.emailForm = self.emailForm(initial={'email' : request.user.email});
        self.passwordForm = self.passwordForm(user = request.user);
        self.deactivateForm = self.deactivateForm(initial = {'is_active' : True});
        return render(request, self.template_name, self.get_context_data(request));
    
    @method_decorator(login_required)    
    def post(self, request, *args, **kwargs):
        if ('change-name' in request.POST):
            self.nameForm = self.changeName(self.nameForm(request.POST));
            return redirect(request.user);
        elif ('change-email' in request.POST):
            self.emailForm = self.changeEmail(self.emailForm(request.POST));
            return redirect(request.user);
        elif ('change-password' in request.POST):
            self.passwordForm = self.passwordForm(request.POST);
            self.changePassword(self.passwordForm(request.POST));
            return redirect(request.user);
        elif ('deactivate-account' in request.POST):
            self.deactivateForm = self.deactivateAccount(self.deactivateForm(request.POST));
            return redirect('sign_out')
        return render(request, self.template_name, self.get_context_data(request));
        
    def get_context_data(self, request):
        context = {
            'change_name_form' : self.nameForm,
            'change_email_form' : self.emailForm,
            'password_form' : self.passwordForm,
            'deactivate_form' : self.deactivateForm,
        }
        return context;
                
    def changeName(self, form):
        if (form.is_valid()):
            self.request.user.first_name = form.cleaned_data['first_name'];
            self.request.user.last_name = form.cleaned_data['last_name'];
            self.request.user.userprofile.last_time_name_was_changed = datetime.now();
            self.request.user.save();
            self.request.user.userprofile.save();
        return form;
        
    def changeEmail(self, form):
        if (form.is_valid()):
            self.request.user.email = form.cleaned_data['email'];
            self.request.user.save();
        return form;
        
    def changePassword(self, form):
        if (form.is_valid()):
            self.request.user.set_password(form.cleaned_data['new_password']);
            self.request.user.save();
        return form;
        
    def deactivateAccount(self, form):
        if (form.is_valid()):
            self.request.user.is_active = False;
            sign_out(self.request)
        return form;
    
    
        
    
    
    
    