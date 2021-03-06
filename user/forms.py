from django.contrib.auth.models import User;
from user.models import Profile;
from django import forms;
from django.contrib.auth import authenticate;
from annoying.functions import get_object_or_None;
from .choices import STATES;
from ourjobfund.acceptable_urls import URLS;
import re;

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder' : 'Username or Email'}));
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}));
    prefix = "login";
    #This is honey pot
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'make-this-disappear'}), initial="", required=False);

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data.get('username_or_email');
        user = get_object_or_None(User, email=username_or_email);
        if (user is None):
            user = get_object_or_None(User, username=username_or_email);
        if (user is None):
            raise forms.ValidationError('Your username or email is incorrect.');
        return username_or_email;    
            
    def clean_password(self):
        username_or_email = self.cleaned_data.get('username_or_email');
        password = self.cleaned_data.get('password');
        user = get_object_or_None(User, email=username_or_email);
        if (user is None):
            user = get_object_or_None(User, username=username_or_email);
        if (not user or (authenticate(username=user.username, password=password) is None)):
            raise forms.ValidationError('Your password is incorrect.');
        return password;
        
    def clean_username(self):
        if (not self.cleaned_data.get('username') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
        
class SignUpForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Email'}));
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Username'}));
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder' : 'Password'}));
    repeat_password = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder' : 'Repeat Password'}));
    age_checkbox = forms.BooleanField(label='Check here to verify you are at least 13 years old');
    #This is honey pot
    other_username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'make-this-disappear'}), initial="", required=False);\
    prefix = "signup";
    
    class Meta:
        model = User;
        fields = ['username', 'email', 'password'];
        
    def clean_username(self):
        username = self.cleaned_data.get('username');
        if (len(username) > 150):
            raise forms.ValidationError('Your first name must not exceed 150 characters.');
        elif (not re.match(r'^[A-Za-z0-9_]+$', username)):
            raise forms.ValidationError('Your username may only include alphanumeric characters, "_", or "-".');
        elif (username in URLS.values()):
            raise forms.ValidationError('You cannot use the username ' + username);
        return username;
        
    def clean_email(self):
        email = self.cleaned_data.get('email');
        if (User.objects.filter(email=email).exists()):
            raise forms.ValidationError('A user already has that email');
        return email;
        
    def clean_password(self):
        password = self.cleaned_data.get('password');
        if (len(password) < 9):
            raise forms.ValidationError('Your password must contain at least 9 characters.');
        if (not re.match(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d!@#\$%\^&\*\(\)]{9,}$', password)):
            raise forms.ValidationError('Your password must contain at least one uppercase letter, lowercase letter, number, and a special character (!, @, #, $, %, ^, &, *, (, or ))');
        return password;
        
    def clean_repeat_password(self):
        password = self.cleaned_data.get('password');
        repeat_password = self.cleaned_data.get('repeat_password');
        if (not repeat_password or password != repeat_password):
            raise forms.ValidationError("Passwords do not match");
        return repeat_password;
        
    def clean_other_username(self):
        if (not self.cleaned_data.get('other_username') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
        
class ChangeProfileForm(forms.ModelForm):
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}), required=False);
    #contact = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact'}), required=False);
    links = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Links'}), required=False);
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}), required=False);
    
    #This is honey pot
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'make-this-disappear'}), initial="", required=False);
    
    class Meta:
        model = Profile;
        fields = ['location', 'links', 'description']; #contact
    
    def clean_username(self):
        if (not self.cleaned_data.get('username') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
    
class ChangeNameForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class' : 'form-control info', 'size' : '12', 'placeholder' :'First Name'}), required=False);
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class' : 'form-control info', 'size' : '12', 'placeholder' : 'Last Name'}), required=False);
    
    #This is honey pot
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'make-this-disappear'}), initial="", required=False);

    class Meta:
        model = User;
        fields = ['first_name', 'last_name'];
        
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name');
        if (len(first_name) > 30):
            raise forms.ValidationError('Your first name must not exceed 30 characters.');
        if (not re.match(r'^[A-Za-z-\']*$', first_name)):
            raise forms.ValidationError('Your first name may only include alphabetic characters, " - ", or " \' ".');
        return first_name;

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name');
        if (len(last_name) > 30):
            raise forms.ValidationError('Your last name must not exceed 30 characters.');
        if (not re.match(r'^[A-Za-z-\']*$', last_name)):
            raise forms.ValidationError('Your last name may only include alphabetic characters,  " - ", or " \' " .');
        return last_name;
   
    def clean_username(self):
        if (not self.cleaned_data.get('username') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";

class ChangeUsernameForm(forms.ModelForm):
    #This is honey pot
    other_username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control make-this-disappear'}), initial="", required=False);
    
    class Meta:
        model = User;
        fields = ['username'];
        
    def clean_username(self):
        username = self.cleaned_data.get('username');
        if (len(username) > 150):
            raise forms.ValidationError('Your first name must not exceed 150 characters.');
        if (not re.match(r'^[A-Za-z0-9_]+$', username)):
            raise forms.ValidationError('Your username may only include alphanumeric characters or "_".');
        if (get_object_or_None(User, username=username)):
            raise forms.ValidationError('Username is already taken.');
        return username;
        
    def clean_other_username(self):
        if (not self.cleaned_data.get('other_username') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";        
        
class ChangeEmailForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-contol'}), initial="", required=False);
    #This is honey pot
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'make-this-disappear'}), initial="", required=False);
    
    class Meta:
        model = User;
        fields = ['email'];
        
    def clean_email(self):
        email = self.cleaned_data.get('email');
        if (User.objects.filter(email=email).exists()):
            raise forms.ValidationError('A user already has that email');
        return email;
    
    def clean_other_username(self):
        if (not self.cleaned_data.get('other_username') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
            
class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(label="Current Password", widget=forms.PasswordInput);
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput);
    repeat_new_password = forms.CharField(label="Repeat New Password", widget=forms.PasswordInput);
    #This is honey pot
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'make-this-disappear'}), initial="", required=False);
            
    class Meta:
        model = User;
        fields = ['password'];
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None);
        super(ChangePasswordForm, self).__init__(*args, **kwargs);
            
    def clean_password(self):
        password = self.cleaned_data.get('password');
        if (not User.objects.get(username=self.user).check_password(password)):
            raise forms.ValidationError('The current password is incorrect.');
        return password;    
            
    def clean_new_password(self):
        password = self.cleaned_data.get('new_password');
        if (len(password) < 9):
            raise forms.ValidationError('Your password must contain at least 9 characters.');
        if (not re.match(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{9,}$', password)):
            raise forms.ValidationError('Your password must contain at least one uppercase letter, lowercase letter, and number.');
        return password;
        
    def clean_repeat_password(self):
        password = self.cleaned_data.get('new_password');
        repeat_password = self.cleaned_data.get('repeat_password');
        if (not repeat_password or password != repeat_password):
            raise forms.ValidationError("Passwords do not match");
        return repeat_password;
        
    def clean_username(self):
        if (not self.cleaned_data.get('other_username') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
        
class DeactivateAccountForm(forms.ModelForm):
    is_active = forms.BooleanField(initial=False, required=False);
    #This is honey pot
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'make-this-disappear'}), initial="", required=False);
    
    class Meta:
        model = User;
        fields = ['is_active'];
        
    def clean_username(self):
        if (not self.cleaned_data.get('username') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
