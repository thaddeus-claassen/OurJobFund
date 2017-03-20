from django.shortcuts import render, get_object_or_404, redirect;
from django.contrib.auth.models import User;
from django.views.generic import View;
from django.http import JsonResponse, HttpResponse, Http404;
from django.core import serializers;
from django.db.models import Q;
from django.contrib.auth import authenticate, login, logout;
from .forms import UserForm, NewUserForm;
from jobuser.forms import NewWorkJobUpdate;
from .models import UserProfile, Messages, UserMessage;
from jobuser.models import WorkJob, ImageUpload, WorkJobUpdate;
from job.models import Job, UserLogic, UserPledgeFilter, UserWorkerFilter;
from job.views import copy_pledge_filter_job, copy_worker_filter_job;
from datetime import datetime;

def create_user(request):
    if (request.method == 'POST'):
        newUserForm = NewUserForm(request.POST);
        if (newUserForm.is_valid()):
            username = newUserForm.cleaned_data['username'];
            email = newUserForm.cleaned_data['email'];
            password = newUserForm.cleaned_data['password'];
            user = User(username=username, email=email);
            user.set_password(password);
            user.save();
            user = authenticate(username=username, password=password);
            UserProfile(user=user).save();
            UserLogic(user=user).save();
            UserPledgeFilter(user=user).save();
            UserWorkerFilter(user=user).save();
            if user is not None:
                if user.is_active:
                    login(request, user);
                    return render(request, 'user/new_user_just_created.html');
    context = {
        'form' : NewUserForm(), 
    }
    return render(request, 'user/create_user.html', context);            

def search_users(request):
    response = "";
    username = request.GET['username'];
    if (User.objects.filter(username=username).exists()):
        response = "user exists";
    else:
        response = "user does not exist";
    return HttpResponse(response);
    
def get_messages_for_navbar(request):
    messages = None;
    if (request.user.is_authenticated()):
        for message in UserMessage.objects.filter(Q(sender=request.user.username) | Q(receiver=request.user.username)).all():
            if (message.date_viewed == ""):
                message.date_viewed == datetime.now;
        messages = UserMessage.objects.filter(Q(sender=request.user.username) | Q(receiver=request.user.username)).order_by('-date_sent')[:5];
        messages = serializers.serialize('json', messages);
    return HttpResponse(messages, content_type='json/application');
    
def get_num_unviewed_messages(request):
    numMessages = 0;
    if (request.user.is_authenticated()):
        messages = UserMessage.objects.filter(receiver=request.user.username).all();
        for message in messages:
            if (message.date_viewed == ""):
                numMessages = numMessages + 1
    return HttpResponse(numMessages);
    
def verify_username(request):
    usernameExists = None;
    if (request.method == 'GET'):
        username = request.GET['username'];
        if (User.objects.filter(username__iexact=username).exists()):
            usernameExists = 'true';
        else:
            usernameExists = 'false';
    return HttpResponse(usernameExists);

def detail(request, user_username):
    user = get_object_or_404(User, username=user_username);       
    context = {
        'id' : user.id,
        'username' : user_username,
        'email' : user.email,
        'description' : user.userprofile.description,
        'pledge_filter_is_public' :  user.userworkerfilter.is_public,
        'worker_filter_is_public' :  user.userpledgefilter.is_public,
    }
    return render(request, 'user/detail.html', context);
    
def get_user_info(request):
    data = {};
    if (request.is_ajax()):
        user_id = request.GET['user_id'];
        user = get_object_or_404(User, pk=user_id);
        data['first_name'] = user.first_name;
        data['last_name'] = user.last_name;
        data['city'] = user.userprofile.city;
        data['state'] = user.userprofile.state;
        data['description'] = user.userprofile.description;
    return JsonResponse(data, safe=False);
    
def add_dependent(request):
    response = "Dependent Error";
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            username = request.POST['username'];
            password = request.POST['password'];
            newUser = User(username=username, email=request.user.email);
            newUser.set_password(password);
            newUser.save();
            UserProfile(user=newUser, is_dependent=True, dependent_on=request.user).save();
            UserLogic(user=newUser).save();
            UserPledgeFilter(user=newUser).save();
            UserWorkerFilter(user=newUser).save();
            response = "Dependent Created";
    return HttpResponse(response);
    
def save_description(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            request.user.userprofile.description = request.POST['description'];
            request.user.userprofile.save();
    return HttpResponse('Done!');
    
def send_message(request):
    response = "Failure";
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            sender = request.user;
            receiver = User.objects.get(username=request.POST['receiver']);
            messages = haveMessages(sender, receiver);
            if (messages == None):
                messages = Messages(userA=sender, userB=receiver);
                messages.save();
            message = request.POST['message'];
            usermessage = UserMessage(twoUsers=messages, message=message, sender=sender.username, receiver=receiver.username).save();
            response = "Success";
    return HttpResponse(response);
    
def messages(request, user_username):
    if (request.user.is_authenticated()):
        other_user = get_object_or_404(User, username=user_username);
        messages = haveMessages(request.user, other_user);
        if (messages != None):
            context = {
                'other_user' : other_user,
                'messages' : messages.usermessage_set.all(),
            };
            return render(request, 'user/messages.html', context);
    return detail(request, user_username);
    
def get_messages(request):
    messages = None;
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            otherUser = get_object_or_404(User, username=request.POST['other_user']);
            messages = getOrderedMessages(request.user, otherUser, 50);
            if (messages != None):
                messages = serializers.serialize('json', messages);
    return HttpResponse(messages, content_type="application/json");
    
def view_messages_by_user(request):
    if (request.user.is_authenticated()):
        context = {
            'most_recent_messages' : get_recent_messages(request.user),
        }
        return render(request, 'user/view_messages_by_user.html', context);  
    return Http404();
        
def get_recent_messages(user):
    messagesQuery = Messages.objects.filter(Q(userA=user) | Q(userB=user)).order_by('-most_recent_sent');
    recentMessages = UserMessage.objects.none();
    for messages in messagesQuery:
        recentMessages = recentMessages | messages.usermessage_set.order_by('-date_sent')[:1];
    return recentMessages;
    
def change_public_pledge_filter(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            request.user.userworkerfilter.is_public = not request.user.userworkerfilter.is_public;
            request.user.userworkerfilter.save();
    return HttpResponse("Finished!");
    
def change_public_worker_filter(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated()):
            request.user.userpledgefilter.is_public = not request.user.userpledgefilter.is_public;
            request.user.userpledgefilter.save();
    return HttpResponse("Finished!");
    
def copy_pledge_filter(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated):
            otherUser = get_object_or_404(User, pk=request.POST['user_id']);
            copy_pledge_filter_job(request.user, otherUser);
    return HttpResponse('Finished!');
    
def copy_worker_filter(request):
    if (request.method == 'POST'):
        if (request.user.is_authenticated):
            otherUser = get_object_or_404(User, pk=request.POST['user_id']);
            copy_worker_filter_job(request.user, otherUser);
    return HttpResponse('Finished!');
        
def haveMessages(user1, user2):
    messages = None;
    if (user1.messagesA.filter(userB=user2).exists()):
        messages = user1.messagesA.get(userB=user2);
    elif (user1.messagesB.filter(userA=user2).exists()):
        messages = user1.messagesB.get(userA=user2);
    return messages;
    
def getOrderedMessages(user1, user2, numMessages):
    messages = None;
    if (user1.messagesA.filter(userB=user2).exists()):
        messages = user1.messagesA.get(userB=user2).usermessage_set.order_by('-date_sent')[:numMessages];
    elif (user1.messagesB.filter(userA=user2).exists()):
        messages = user1.messagesB.get(userA=user2).usermessage_set.order_by('-date_sent')[:numMessages];
    data  = {};
    return messages;
        
      
    
    
        