from django.contrib.auth.models import User;
from django.contrib.auth import authenticate, login;
from django.shortcuts import redirect;
from .forms import LoginForm;


def login_form(request):
    context = {};
    if (not request.user.is_authenticated()):
        form = LoginForm;
        context = {'login_form': form};
    return context;