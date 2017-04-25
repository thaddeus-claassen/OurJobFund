from django.contrib.auth.models import User;
from django import forms;
from django.forms import extras;

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput);

    class Meta: 
        model = User;
        fields = ['email', 'password'];
            
        
class NewUserForm(forms.ModelForm):
    password = forms.CharField(label='Password:', widget=forms.PasswordInput);
    repeat_password = forms.CharField(label='Repeat Password:', widget=forms.PasswordInput);
    
    class Meta: 
        model = User;
        fields = ['first_name', 'last_name', 'email', 'password'];
        
    

        
        
