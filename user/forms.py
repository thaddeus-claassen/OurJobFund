from user.models import User, UserProfile;
from django.core.validators import RegexValidator; 
from django import forms;
from django.forms import extras;
import re;

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}));
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}));

    class Meta: 
        model = User;
        fields = ['email', 'password'];
            
        
class NewUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'First Name'}));
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Last Name'}));
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder' : 'Email'}));
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}));
    repeat_password = forms.CharField(label='Repeat Password:', widget=forms.PasswordInput(attrs={'placeholder' : 'Repeat Password'}));
    age_checkbox = forms.BooleanField(label='Check here to verify you are at least 13 years old:');
    
    class Meta: 
        model = User;
        fields = ['first_name', 'last_name', 'email', 'password'];
        
    def clean_email(self):
        email = self.cleaned_data.get('email');
        if (User.objects.filter(email=email).exists()):
            raise forms.ValidationError('A user already has that email');
        return email;
        
    def clean_password(self):
        password = self.cleaned_data.get('password');
        if (len(password) < 9):
            raise forms.ValidationError('Your password must contain at least 9 characters.');
        if (not re.match(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{9,}$', password)):
            raise forms.ValidationError('Your password must contain at least one uppercase letter, lowercase letter, and number');
        return password;
        
    def clean_repeat_password(self):
        password = self.cleaned_data.get('password');
        repeat_password = self.cleaned_data.get('repeat_password');
        if (not repeat_password or password != repeat_password):
            raise forms.ValidationError("Passwords do not match");
        return repeat_password;
        

class DescriptionForm(forms.ModelForm):
        description = forms.CharField(label="Description:", widget=forms.Textarea, max_length=10000);
        
        class Meta:
            model = UserProfile;
            fields = ['description'];

    

        
        
