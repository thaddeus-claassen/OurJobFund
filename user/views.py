from django.shortcuts import render, get_object_or_404, redirect;
from django.contrib.auth.models import User;
from django.views.generic import View;
from django.http import HttpResponse;
from django.contrib.auth import authenticate, login, logout;
from .forms import UserForm, NewUserForm;
from .models import UserProfile;

def create_user(request):
    if (request.method == 'POST'):
        newUserForm = NewUserForm(request.POST);
        if (newUserForm.is_valid()):
            username = newUserForm.cleaned_data['username'];
            password = newUserForm.cleaned_data['password'];
            user = User(username=username);
            user.set_password(password);
            user.save();
            user = authenticate(username=username, password=password);
            if user is not None:
                if user.is_active:
                    login(request, user);
                    return redirect('user/new_user_just_created');
    context = {
        'form' : NewUserForm(), 
    }
    return render(request, 'user/create_user.html', context);            

    
def verify_username(request):
    userNameExists = None;
    if (request.method == 'GET'):
        username = request.GET['username'];
        if (User.objects.filter(username__iexact=username).exists()):
            userNameExists = 'true';
        else:
            userNameExists = 'false';
    return HttpResponse(userNameExists);

def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id);                                       
    context = {              
        'id' : user_id,
        'username' : user.username,
        'email' : user.email,
        'description' : user.userprofile.description,
        'working' : user.working.all(),
        'pledging' : user.pledging.all(),
    }
    return render(request, 'user/detail.html', context);
    

        