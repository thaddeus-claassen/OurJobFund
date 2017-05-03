from django.contrib.auth.models import User;
from django.core.validators import RegexValidator; 
from django import forms;
from django.forms import extras;

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}));
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}));

    class Meta: 
        model = User;
        fields = ['email', 'password'];
            
        
class NewUserForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', validators=[RegexValidator(r'^[a-zA-Z]+$')]);
    last_name = forms.CharField(label='Last Name', validators=[RegexValidator(r'^[a-zA-Z]+$')]);
    email = forms.EmailField(label='Email');
    password = forms.CharField(label='Password:', widget=forms.PasswordInput);
    repeat_password = forms.CharField(label='Repeat Password:', widget=forms.PasswordInput);
    checkbox_input = forms.BooleanField(label='Check here to verify you are at least 13 years old:');
    
    class Meta: 
        model = User;
        fields = ['first_name', 'last_name', 'email', 'password'];
        
    

        
        
