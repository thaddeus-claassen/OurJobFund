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
from .forms import ChangePasswordForm, ChangeNameForm, ChangeEmailForm, LoginForm, SignUpForm, DeactivateAccountForm, ProfileForm, DescriptionForm, ChangeUsernameForm;
from .models import UserProfile;
from job.models import Job;
from datetime import datetime;
from random import randint;
import json;

class LoginView(TemplateView):
    template_name = 'user/login.html';
    login_form = LoginForm();
    sign_up_form = SignUpForm();
    
    def get(self, request, *args, **kwargs):
        if (request.user.is_authenticated()):
            return redirect('user:detail', username=request.user.username);
        else:
            return render(request, self.template_name, self.get_context_data(login_form=self.login_form, sign_up_form=self.sign_up_form));
    
    def post(self, request, *args, **kwargs):
        if (request.user.is_authenticated()):
            return redirect(request.user);
        else:
            login_form = self.login_form;
            if ('sign-in' in request.POST):
                login_form = LoginForm(request.POST);
                if (login_form.is_valid()):
                    user = User.objects.get(email=login_form.cleaned_data['email']);
                    user.is_active = True;
                    login(request, user);
                    return redirect('job:home');
            sign_up_form = self.sign_up_form;
            if ('sign-up' in request.POST):
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
                        return redirect(user);
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

class SearchUsersView(TemplateView):
    template_name = 'user/search.html';
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        search = request.GET['search-users'];
        context = {
            'users' : self.getUsersFromQuery(search, 0),
            'search' : search,
            'total' : self.getTotalNumberOfUsersFromQuery(search),
        };
        return render(request, 'user/search.html', context);
    
    def getUsersFromQuery(self, search, num_searches):
        users = User.objects.all();
        for word in search.split():
            users = users.filter(Q(username__icontains=word) | Q(first_name__istartswith=word) | Q(last_name__istartswith=word));
            start = (50 * num_searches);
            end = start + 50;
        users = users[start:end];
        return users;
        
    def getTotalNumberOfUsersFromQuery(self, search):
        users = User.objects.all();
        for word in search.split():
            users = users.filter(Q(username__icontains=word) | Q(first_name__istartswith=word) | Q(last_name__istartswith=word));
        return users.count();

@login_required
def see_more_users(request):
    if (request.is_ajax()):
        search = request.GET['search'];
        num_searches = request.GET['num_searches'];
        users = getUsersFromQuery(search, num_searches);
        users = serializers.serialize("json", users);
        return HttpResponse(users, content_type="application/json");
    else:
        return Http404();

class DetailView(TemplateView):
    template_name = 'user/detail.html';
    nameForm = ChangeNameForm;
    profileForm = ProfileForm;
    descriptionForm = DescriptionForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username']);
        self.nameForm = self.nameForm(initial={'first_name' : user.first_name, 'last_name' : user.last_name });
        self.profileForm = self.profileForm(initial={
            'city' : user.userprofile.city, 
            'state' : user.userprofile.state,
            'occupation' : user.userprofile.occupation,
            'education' : user.userprofile.education,
            'contact' : user.userprofile.contact,
        });
        self.descriptionForm = self.descriptionForm(initial={'description' : user.userprofile.description});
        return render(request, self.template_name, self.get_context_data());
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if ('info' in request.POST):
            self.nameForm = self.nameForm(request.POST);
            self.profileForm = self.profileForm(request.POST);
            if (self.nameForm.is_valid() and self.profileForm.is_valid()):
                request.user.first_name = self.nameForm.cleaned_data['first_name'];
                request.user.last_name = self.nameForm.cleaned_data['last_name'];
                request.user.save();
                request.user.userprofile.city = self.profileForm.cleaned_data['city'];
                request.user.userprofile.state = self.profileForm.cleaned_data['state'];
                request.user.userprofile.occupation = self.profileForm.cleaned_data['occupation'];
                request.user.userprofile.education = self.profileForm.cleaned_data['education'];
                request.user.userprofile.contact = self.profileForm.cleaned_data['contact'];
                request.user.userprofile.save();
                return redirect(request.user);
        elif ('description' in request.POST):
            self.descriptionForm = self.descriptionForm(request.POST);
            if (self.descriptionForm.is_valid()):
                request.user.userprofile.description = self.descriptionForm.cleaned_data['description'];
                request.user.userprofile.save();
                return redirect(request.user);
        elif ('stripeToken' in request.POST):
            self.pay(request, job, jobuser);
            return redirect('user:confirmation', username=get_object_or_404(User, username=kwargs['username']));
        elif ('delete-stripe' in request.POST):
            request.user.userprofile.stripe_account_id = "";
            request.user.userprofile.save();
        return render(request, self.template_name, self.get_context_data({'username' : kwargs['username']}));
        
    def pay(self, request, job, jobuser):
        receiver_pk = request.POST['pay_to'];
        stripe.api_key = STRIPE_TEST_SECRET_KEY;
        token = request.POST['stripeToken'];
        amount_paying_in_cents = int(request.POST['pay_amount']);
        charge = stripe.Charge.create(
            amount = amount_paying_in_cents,
            currency = "usd",
            description = "Does this charge work?",
            source = token,
        );
        amount_paying_in_dollars = float(amount_paying_in_cents) / 100;
        payment = Pay(jobuser=jobuser, receiver=jobuser.user, amount=amount_paying_in_dollars);
        payment.save();
        jobuser.amount_paid = jobuser.amount_paid + amount_paying_in_dollars;
        jobuser.save();
        receiver_jobuser = JobUser.objects.get(user=User.objects.get(id=receiver_pk), job=job);
        receiver_jobuser.amount_received = receiver_jobuser.amount_received + amount_paying_in_dollars;
        receiver_jobuser.save();
        job.paid = job.paid + amount_paying_in_dollars;
        job.save();
        
    def get_context_data(self, *args, **kwargs):
        user = get_object_or_None(User, username=self.kwargs['username']);
        context = {
            'detail_user' : user,
            'name_form' : self.nameForm,
            'profile_form' : self.profileForm,
            'description_form' : self.descriptionForm,
            'current_jobusers' : user.jobuser_set.filter(Q(job__pledged=0) | Q(job__pledged__gt=F('job__paid'))),
            'finished_jobusers' : user.jobuser_set.filter(Q(job__pledged__gt=0) & Q(job__pledged__lte=F('job__paid'))),
        }
        return context;
        
class AccountView(TemplateView):
    template_name = 'user/account.html';
    usernameForm = ChangeUsernameForm;
    emailForm = ChangeEmailForm;
    passwordForm = ChangePasswordForm;
    deactivateForm = DeactivateAccountForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if ((datetime.now() - request.user.userprofile.last_time_username_was_changed.replace(tzinfo=None)).days >= 180):
            self.usernameForm = self.usernameForm(initial={'username' : request.user.username});
        self.emailForm = self.emailForm(initial={'email' : request.user.email});
        self.passwordForm = self.passwordForm;
        self.deactivateForm = self.deactivateForm(initial={'is_active' : True});
        return render(request, self.template_name, self.get_context_data(request));
    
    @method_decorator(login_required)    
    def post(self, request, *args, **kwargs):
        if ('change-name' in request.POST):
            self.usernameForm = self.changeUsername(self.usernameForm(request.POST));
        elif ('change-email' in request.POST):
            self.emailForm = self.changeEmail(self.emailForm(request.POST));
        elif ('change-password' in request.POST):
            self.passwordForm = self.changePassword(self.passwordForm(request.POST, user=request.user));
        elif ('deactivate-account' in request.POST):
            self.deactivateForm = self.deactivateAccount(self.deactivateForm(request.POST));
        return render(request, self.template_name, self.get_context_data(request));
        
    def get_context_data(self, request):
        context = {
            'change_username_form' : self.usernameForm,
            'change_email_form' : self.emailForm,
            'change_password_form' : self.passwordForm,
            'deactivate_form' : self.deactivateForm,
        }
        return context;
                
    def changeUsername(self, form):
        if (form.is_valid()):
            self.request.user.username = form.cleaned_data['username'];
            self.request.user.save();
            self.request.user.userprofile.last_time_name_was_changed = datetime.now();
            self.request.user.userprofile.save();
            return redirect('user:account');
        return form;
        
    def changeEmail(self, form):
        if (form.is_valid()):
            self.request.user.email = form.cleaned_data['email'];
            self.request.user.save();
            return redirect('user:account');
        return form;
        
    def changePassword(self, form):
        if (form.is_valid()):
            self.request.user.set_password(form.cleaned_data['new_password']);
            self.request.user.save();
            return redirect('user:account');
        return form;
        
    def deactivateAccount(self, form):
        if (form.is_valid()):
            self.request.user.is_active = False;
            self.request.user.save();
            return redirect('user:sign_out');
        return form;
    
    
        
    
    
    
    