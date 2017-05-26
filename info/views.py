from django.contrib.auth.decorators import login_required;
from django.shortcuts import render;

@login_required
def account(request):
    return render(request, 'info/account.html');

def about(request):
    return render(request, 'info/about.html');
    
def contact(request):
    return render(request, 'info/contact.html');
    
def termsOfAgreement(request):
    return render(request, 'info/terms-of-agreement.html');
