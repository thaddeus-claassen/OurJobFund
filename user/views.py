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
    new_user_form = SignUpForm;
    login_form = LoginForm;
    
    def get(self, request, *args, **kwargs):
        if (request.user.is_authenticated()):
            return redirect('user:detail', username=request.user.username);
        else:
            return render(request, self.template_name, self.get_context_data(login_form=self.login_form, new_user_form=self.new_user_form));
    
    def post(self, request, *args, **kwargs):
        if (request.user.is_authenticated()):
            return redirect(request.user);
        else:
            login_form = self.login_form;
            if ('login' in request.POST):
                login_form = login_form(request.POST);
                if (login_form.is_valid()):
                    email = userForm.cleaned_data['email'];
                    if (email != "" and User.objects.filter(email=email).exists()):
                        user = authenticate(username=User.objects.get(email=email).username, password=userForm.cleaned_data['password']);
                        if (user is not None):
                            user.is_active = True;
                            login(request, user);
                            return redirect('job:home');
            new_user_form = self.new_user_form;
            if ('sign-up' in request.POST):
                new_user_form = new_user_form(request.POST);
                if (new_user_form.is_valid()):
                    user = new_user_form.save(commit=False);
                    user.email = new_user_form.cleaned_data['email'];
                    user.username = new_user_form.cleaned_data['username'];
                    password = new_user_form.cleaned_data['password'];
                    user.set_password(password);
                    user.save();
                    user = authenticate(username=user.username, password=password);
                    if (user is not None):
                        login(request, user);
                        return redirect(user);
            return render(request, self.template_name, self.get_context_data(login_form=login_form, new_user_form=new_user_form));
        
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs);
        context['login_form'] = kwargs['login_form'];
        context['new_user_form'] = kwargs['new_user_form'];
        return context;

@login_required
def sign_out(request):
    logout(request);
    return redirect('user:login');

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
        users = users.filter(Q(username__icontains=word) | Q(first_name__istartswith=word) | Q(last_name__istartswith=word));
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
        if ('first_name' in request.POST):
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
        receiver_username = request.POST['pay_to'];
        stripe.api_key = STRIPE_TEST_SECRET_KEY;
        token = request.POST['stripeToken'];
        amount_paying = float(request.POST['pay_amount']);
        charge = stripe.Charge.create(
            amount = 100 * amount_paying,
            currency = "usd",
            description = "Does this charge work?",
            source = token,
        );
        payment = Pay(jobuser=jobuser, receiver=jobuser.user, amount=float(amount_paying));
        payment.save();
        jobuser.amount_paid = jobuser.amount_paid + amount_paying;
        jobuser.save();
        receiver_jobuser = JobUser.objects.get(user=User.objects.get(username=receiver_username), job=job);
        receiver_jobuser.amount_received = receiver_jobuser.amount_received + amount_paying;
        receiver_jobuser.save();
        job.paid = job.paid + amount_paying;
        job.save();
        create_update_by_paying(payment);
        
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

@login_required        
def save_input(request, username):
    if (request.user.username == username and request.is_ajax() and request.method == "POST"):
        id = request.POST['id'];
        value = request.POST['value'];
        if (id == 'id_first_name'):
            request.user.first_name = value;
        elif (id == 'id_last_name'):
            request.user.last_name = value;
        elif (id == 'id_city'):
            request.user.userprofile.city = value;
        elif (id == 'id_state'):
            request.user.userprofile.state = value;
        elif (id == 'id_education'):
            request.user.userprofile.education = value;                
        elif (id == 'id_occupation'):
            request.user.userprofile.occupation = value;
        elif (id == 'id_contact'):
           request.user.userprofile.contact = value;                
        elif (id == 'id_description'):
            request.user.userprofile.description = value;
        request.user.save();
        request.user.userprofile.save();
        return HttpResponse();
    else:
        return Http404();
        
        
@login_required
def payment_confirmation(request, job_random_string):
    job = get_object_or_404(Job, random_string = job_random_string);
    context = {
        'job' : job,
    }
    return render(request, 'job/confirmation.html', context);
        
class AccountView(TemplateView):
    template_name = 'user/account.html';
    usernameForm = ChangeUsernameForm;
    emailForm = ChangeEmailForm;
    passwordForm = ChangePasswordForm;
    deactivateForm = DeactivateAccountForm;
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if ((datetime.now() - request.user.userprofile.last_time_username_was_changed.replace(tzinfo=None)).days >= 180):
            self.usernameForm = self.usernameForm(initial = {'username' : request.user.username});
        self.emailForm = self.emailForm(initial={'email' : request.user.email});
        self.passwordForm = self.passwordForm(user = request.user);
        self.deactivateForm = self.deactivateForm(initial = {'is_active' : True});
        return render(request, self.template_name, self.get_context_data(request));
    
    @method_decorator(login_required)    
    def post(self, request, *args, **kwargs):
        if ('change-name' in request.POST):
            self.usernameForm = self.changeUsername(self.usernameForm(request.POST));
            return redirect(request.user);
        elif ('change-email' in request.POST):
            self.emailForm = self.changeEmail(self.emailForm(request.POST));
            return redirect(request.user);
        elif ('change-password' in request.POST):
            self.passwordForm = self.changePassword(self.passwordForm(request.POST, user=request.user));
            return redirect(request.user);
        elif ('deactivate-account' in request.POST):
            self.deactivateForm = self.deactivateAccount(self.deactivateForm(request.POST));
            return redirect('sign_out');
        return render(request, self.template_name, self.get_context_data(request));
        
    def get_context_data(self, request):
        context = {
            'change_username_form' : self.usernameForm,
            'change_email_form' : self.emailForm,
            'password_form' : self.passwordForm,
            'deactivate_form' : self.deactivateForm,
        }
        return context;
                
    def changeUsername(self, form):
        if (form.is_valid()):
            self.request.user.username = form.cleaned_data['username'];
            self.request.user.save();
            self.request.user.userprofile.last_time_name_was_changed = datetime.now();
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
    
    
        
    
    
    
    