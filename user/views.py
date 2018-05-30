from django.contrib.auth.decorators import login_required;
from django.db.models.functions import Lower;
from django.contrib.auth.models import User;
from rest_framework.renderers import JSONRenderer;
from django.utils.decorators import method_decorator;
from django.views.generic import TemplateView;
from jobuser.serializers import JobUserSerializer;
from django.contrib.auth import authenticate, login, logout;
from ourjobfund.settings import STRIPE_TEST_SECRET_KEY, STATIC_ROOT;
from annoying.functions import get_object_or_None;
from django.db.models import Q, F;
from django.shortcuts import render, get_object_or_404, redirect;
from django.forms import formset_factory;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from job.models import Job;
from datetime import datetime;
from .models import Profile;
from .forms import ChangeUsernameForm, ChangePasswordForm, ChangeEmailForm, DeactivateAccountForm, LoginForm, SignUpForm, ChangeProfileForm, ChangeNameForm;
import json, stripe;

class LoginView(TemplateView):
    template_name = 'user/login.html';
    login_form = LoginForm;
    sign_up_form = SignUpForm;
    
    def get(self, request, *args, **kwargs):
        if (request.user.is_authenticated):
            return redirect('home');
        else:
            return render(request, self.template_name, self.get_context_data(login_form=self.login_form, sign_up_form=self.sign_up_form));
    
    def post(self, request, *args, **kwargs):
        login_form = self.login_form;
        sign_up_form = self.sign_up_form;
        if ('sign-in' in request.POST):
            login_form = LoginForm(request.POST);
            if (login_form.is_valid()):
                user = get_object_or_None(User, email=login_form.cleaned_data['username_or_email']);
                if (user is None):
                    user = get_object_or_None(User, username=login_form.cleaned_data['username_or_email']);
                user.is_active = True;
                login(request, user);
                return redirect('home');
        elif ('sign-up' in request.POST):
            sign_up_form = SignUpForm(request.POST);
            if (sign_up_form.is_valid()):
                user = sign_up_form.save(commit=False);
                user.email = sign_up_form.cleaned_data['email'];
                user.username = sign_up_form.cleaned_data['username'];
                password = sign_up_form.cleaned_data['password'];
                user.set_password(password);
                user.save();
                user = authenticate(username=user.username, password=password);
                if (user is not None):
                    login(request, user);
                    return redirect('user:login');
        return render(request, self.template_name, self.get_context_data(login_form=login_form, sign_up_form=sign_up_form));
        
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs);
        context['login_form'] = kwargs['login_form'];
        context['sign_up_form'] = kwargs['sign_up_form'];
        return context;

@login_required
def sign_out(request):
    logout(request);
    return redirect('user:login');

def search_user(request):
    if (request.is_ajax()):
        username = request.GET['username'];
        user = get_object_or_None(User, username=username);
        data = {};
        if (user):
            data['username'] = user.username;
        else:
            data = "";
        return HttpResponse(json.dumps(data), content_type="application/json");
    else:
        return Http404();
        
class DetailView(TemplateView):
    template_name = 'user/detail.html';
    
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username']);
        return render(request, self.template_name, self.get_context_data(request, user=user));
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if ('delete-stripe' in request.POST):
            request.user.profile.stripe_account_id = "";
            request.user.profile.save();
        return render(request, self.template_name, self.get_context_data(request, user=request.user, description_form = description_form, name_form=name_form));
        
    def get_context_data(self, request, *args, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs);
        user = kwargs['user'];
        context['detail_user'] = user;
        context['current'] =  user.jobuser_set.filter(job__is_finished=False);
        context['completed'] = user.jobuser_set.filter(job__is_finished=True);
        return context;
 
def add_to_detail_table(request, username):
    if (request.is_ajax()):
        user = get_object_or_404(User, username=username);
        numSearches = int(request.GET['num_searches']);
        table = request.GET['table'];
        column = request.GET['column'];
        order = request.GET['order'];
        if (table == 'current'):
            data = user.jobuser_set.filter(job__is_finished=False);
        else:
            data = user.jobuser_set.filter(job__is_finished=True);
        if (column == 'title'):
            if (order == 'ascending'):
                data = data.order_by(Lower('job__title'))[50 * numSearches : 50 * (numSearches + 1)][::-1];
            else:
                data = data.order_by(Lower('job__title'))[50 * numSearches : 50 * (numSearches + 1)];
        else:
            if (order == 'ascending'):
                data = data.order_by(column)[50 * numSearches : 50 * (numSearches + 1)][::-1];
            else:
                data = data.order_by(column)[50 * numSearches : 50 * (numSearches + 1)];
        serializer = JobUserSerializer(data, many=True);
        json = JSONRenderer().render(serializer.data);
        return HttpResponse(json, 'application/json');
    else:
        return Http404();
        
class EditProfileView(TemplateView):
    template_name = 'user/edit_profile.html';
    profile_form = ChangeProfileForm;
    name_form = ChangeNameForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if (request.user.username == kwargs['username']):
            name_form = self.name_form(initial={'first_name' : request.user.first_name, 'last_name' : request.user.last_name});
            profile_form = self.profile_form(initial={'location': request.user.profile.location, 'description': request.user.profile.description});
            return render(request, self.template_name, self.get_context_data(name_form=name_form, profile_form=profile_form));
        else:
            return redirect('user:edit_profile', username=request.user.username);

    @method_decorator(login_required)      
    def post(self, request ,*args, **kwargs):
        name_form = self.name_form(request.POST);
        profile_form = self.profile_form(request.POST);
        if (profile_form.is_valid() and name_form.is_valid()):
            request.user.first_name = name_form.cleaned_data['first_name'];
            request.user.last_name = name_form.cleaned_data['last_name'];
            request.user.save();
            request.user.profile.location = profile_form.cleaned_data['location'];
            request.user.profile.description = profile_form.cleaned_data['description'];
            request.user.profile.save();
            return redirect('user:detail', username=request.user.username);
        else:
            return render(request, self.template_name, self.get_context_data(name_form=name_form, profile_form=profile_form));
            
    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs);
        context['name_form'] = kwargs['name_form'];
        context['profile_form'] = kwargs['profile_form'];
        return context;
        
class AccountView(TemplateView):
    template_name = 'user/account.html';
    usernameForm = ChangeUsernameForm;
    emailForm = ChangeEmailForm;
    passwordForm = ChangePasswordForm;
    deactivateForm = DeactivateAccountForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        usernameForm = self.usernameForm(initial={'username' : request.user.username});
        emailForm = self.emailForm(initial={'email' : request.user.email});
        passwordForm = self.passwordForm;
        deactivateForm = self.deactivateForm(initial={'is_active' : True});
        return render(request, self.template_name, self.get_context_data(request, usernameForm=usernameForm, emailForm=emailForm, passwordForm=passwordForm, deactivateForm=deactivateForm));
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        usernameForm = self.usernameForm;
        emailForm = self.emailForm;
        passwordForm = self.passwordForm;
        deactivateForm = self.deactivateForm;
        if ('change-username' in request.POST):
            usernameForm = usernameForm(request.POST);
            print("Form is valid: " + str(usernameForm.is_valid()))
            if (usernameForm.is_valid()):
                print(usernameForm.cleaned_data['username'])
                self.request.user.username = usernameForm.cleaned_data['username'];
                self.request.user.save();
                self.request.user.profile.last_time_username_was_changed = datetime.now();
                self.request.user.profile.save();
                return redirect('user:account');
        elif ('change-email' in request.POST):
            emailForm = emailForm(request.POST);
            if (emailForm.is_valid()):
                self.request.user.email = emailForm.cleaned_data['email'];
                self.request.user.save();
                return redirect('user:account');
        elif ('change-password' in request.POST):
            passwordForm = passwordForm(request.POST, user=request.user);
            if (passwordForm.is_valid()):
                self.request.user.set_password(passwordForm.cleaned_data['new_password']);
                self.request.user.save();
                login(self.request, request.user);
                return redirect('user:account');
        elif ('deactivate-account' in request.POST):
            deactivateForm = deactivateForm(request.POST);
            if (deactivateForm.is_valid()):
                self.request.user.is_active = False;
                self.request.user.save();
                return redirect('user:sign_out');
        return render(request, self.template_name, self.get_context_data(request, usernameForm=usernameForm, emailForm=emailForm, passwordForm=passwordForm, deactivateForm=deactivateForm));
        
    def get_context_data(self, request, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs);
        context['change_username_form'] = kwargs['usernameForm'];
        context['next_time_username_can_be_changed'] = 180 - (datetime.now() - request.user.profile.last_time_username_was_changed.replace(tzinfo=None)).days;
        context['change_email_form'] = kwargs['emailForm'];
        context['change_password_form'] = kwargs['passwordForm'];
        context['deactivate_form'] = kwargs['deactivateForm'];
        return context;
    
@login_required
def stripe(request):
    username = request.GET.get('state', None);
    if (username is not None):
        user = get_object_or_404(User, username=username);
        if (user.username == request.user.username):
            code = request.GET.get('code', None);
            request.user.profile.stripe_account_id = code;
            request.user.profile.save();
            return redirect('user:detail', username=username);
        else:
            Http404();
    else:
        return Http404();
    
    
    
    