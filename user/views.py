from django.shortcuts import render, get_object_or_404;
from django.contrib.auth.models import User;
from .models import UserProfile;

def index(request, user_id):
    user = get_object_or_404(User, pk=user_id);                                       
    context = {                                                                       
        'username' : user.username,
        'email' : user.email,
        'description' : user.userprofile.description,
        'working' : user.working.all(),
        'pledging' : user.pledging.all(),
    }
    return render(request, 'user/index.html', context);
    
def create_user(request):
    return render(request, 'user/create_user.html');
