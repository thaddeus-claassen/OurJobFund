from django.contrib.auth.decorators import login_required;
from django.contrib.auth.models import User;
from django.utils.decorators import method_decorator;
from django.views.generic import TemplateView;
from django.contrib.auth import authenticate, login, logout;
from ourjobfund.settings import STRIPE_TEST_SECRET_KEY, STATIC_ROOT;
from annoying.functions import get_object_or_None;
from django.db.models import Q, F;
from django.shortcuts import render, get_object_or_404, redirect;
from django.forms import formset_factory;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from pay.models import Pay;
from job.models import Job;
from datetime import datetime;
from .models import Profile;
from random import randint;
from .forms import ChangePasswordForm, ChangeNameForm, ChangeEmailForm, LoginForm, SignUpForm, DeactivateAccountForm, ProfileForm, DescriptionForm, ChangeUsernameForm;
import json, stripe;

def payment_confirmation(request, job_random_string):
    job = get_object_or_404(Job, random_string = job_random_string);
    return render(request, 'pay/confirmed.html', {'job' : job});