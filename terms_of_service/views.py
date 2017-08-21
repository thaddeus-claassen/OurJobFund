from django.shortcuts import render
    
def termsOfService(request):
    return render(request, 'terms_of_service/terms-of-service.html');
