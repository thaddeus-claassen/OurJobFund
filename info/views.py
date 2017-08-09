from django.contrib.auth.decorators import login_required;
from django.shortcuts import render;

def about(request):
    return render(request, 'info/about.html');
    
def contact(request):
    return render(request, 'info/contact.html');
    
def termsOfAgreement(request):
    return render(request, 'info/terms-of-agreement.html');
