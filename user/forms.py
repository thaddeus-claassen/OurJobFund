from django.contrib.auth.models import User;
from .models import WorkJobUpdate;
from django import forms;
from django.forms import extras;

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput);

    class Meta: 
        model = User;
        fields = ['email', 'password'];
            
        
class NewUserForm(forms.ModelForm): 
    username = forms.CharField(label='Username:', max_length=100);
    email = forms.EmailField(label='Email:');
    password = forms.CharField(label='Password:', widget=forms.PasswordInput);
    repeat_password = forms.CharField(label='Repeat Password:', widget=forms.PasswordInput);
    
    class Meta: 
        model = User;
        fields = ['username', 'email', 'password'];
        
class NewWorkJobUpdate(forms.ModelForm):
    title = forms.CharField(label='Title:', max_length=100);
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}));
    description = forms.CharField(label='Description:', widget=forms.Textarea);
    
    class Meta:
        model = WorkJobUpdate;
        fields = ['title', 'description'];
    

        
        
