from django.contrib.auth.models import User;
from user.models import UserProfile
from django import forms;
from .choices import STATES, PAYMENT_METHODS;
import re;

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}));
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder' : 'Email'}));
    protection = forms.CharField(label="", widget=forms.HiddenInput(), initial="", required=False);

    class Meta:
        model = User;
        fields = ['email', 'password'];
    
    def clean_protection(self):
        if (not self.cleaned_data.get('protection') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
    
class NewUserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder' : 'Email'}));
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Username'}));
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}));
    repeat_password = forms.CharField(label='Repeat Password:', widget=forms.PasswordInput(attrs={'placeholder' : 'Repeat Password'}));
    age_checkbox = forms.BooleanField(label='Check here to verify you are at least 13 years old:');
    protection = forms.CharField(label="", widget=forms.HiddenInput(), initial="", required=False);
    
    class Meta:
        model = User;
        fields = ['username', 'email', 'password'];
        
    def clean_username(self):
        username = self.cleaned_data.get('username');
        if (len(username) > 150):
            raise forms.ValidationError('Your first name must not exceed 150 characters.');
        if (not re.match(r'^[A-Za-z0-9_]+$', username)):
            raise forms.ValidationError('Your username may only include alphanumeric characters, "_", or "-".');
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
        if (not re.match(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{9,}$', password)):
            raise forms.ValidationError('Your password must contain at least one uppercase letter, lowercase letter, and number');
        return password;
        
    def clean_repeat_password(self):
        password = self.cleaned_data.get('password');
        repeat_password = self.cleaned_data.get('repeat_password');
        if (not repeat_password or password != repeat_password):
            raise forms.ValidationError("Passwords do not match");
        return repeat_password;
        
    def clean_protection(self):
        if (not self.cleaned_data.get('protection') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
            
class ProfileForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput(attrs={'class' : 'info', 'size' : '12'}), required=False);
    state = forms.ChoiceField(choices=STATES, widget=forms.Select(attrs={'class' : 'info'}), required=False);
    education = forms.CharField(widget=forms.TextInput(attrs={'class' : 'info', 'size' : '12'}), required=False);
    occupation = forms.CharField(widget=forms.TextInput(attrs={'class' : 'info', 'size' : '12'}), required=False);
    contact = forms.CharField(widget=forms.TextInput(attrs={'class' : 'info', 'size' : '12'}), required=False);
    preferred_payment = forms.ChoiceField(choices=PAYMENT_METHODS, widget=forms.Select(attrs={'class' : 'info'}));
    protection = forms.CharField(label="", widget=forms.HiddenInput(), initial="", required=False);
    
    class Meta:
        model = UserProfile;
        fields = ['city', 'state', 'education', 'occupation', 'contact', 'preferred_payment'];    
    
    def clean_protection(self):
        if (not self.cleaned_data.get('protection') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
    
class ChangeNameForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class' : 'info', 'size' : '12'}), required=False);
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class' : 'info', 'size' : '12'}), required=False);
    protection = forms.CharField(label="", widget=forms.HiddenInput(), initial="", required=False);

    class Meta: 
        model = User;
        fields = ['first_name', 'last_name'];
        
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name');
        if (len(first_name) > 30):
            raise forms.ValidationError('Your first name must not exceed 30 characters.');
        if (not re.match(r'^[A-Za-z-]{1,30}$', first_name)):
            raise forms.ValidationError('Your first name may only include alphabetic characters or "-".');
        return first_name;

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name');
        if (len(last_name) > 30):
            raise forms.ValidationError('Your last name must not exceed 30 characters.');
        if (not re.match(r'^[A-Za-z]{1,30}$', last_name)):
            raise forms.ValidationError('Your first name may only include alphabetic characters or "-".');
        return last_name;
   
    def clean_protection(self):
        if (not self.cleaned_data.get('protection') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
        
class DescriptionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea);
    protection = forms.CharField(label="", widget=forms.HiddenInput(), initial="", required=False);

    class Meta:
        model = UserProfile;
        fields = ['description'];    

    def clean_protection(self):
        if (not self.cleaned_data.get('protection') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";        
        
class ChangeUsernameForm(forms.ModelForm):
    protection = forms.CharField(label="", widget=forms.HiddenInput(), initial="", required=False);
    
    class Meta:
        model = User;
        fields = ['username'];
        
    def clean_protection(self):
        if (not self.cleaned_data.get('protection') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";        
        
class ChangeEmailForm(forms.ModelForm):
    email = forms.CharField(max_length=30, required=False);
    protection = forms.CharField(label="", widget=forms.HiddenInput(), initial="", required=False);
    
    class Meta:
        model = User;
        fields = ['email'];
        
    def clean_email(self):
        email = self.cleaned_data.get('email');
        if (User.objects.filter(email=email).exists()):
            raise forms.ValidationError('A user already has that email');
        return email;
    
    def clean_protection(self):
        if (not self.cleaned_data.get('protection') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
            
class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(label="Current Password", widget=forms.PasswordInput);
    new_password = forms.CharField(widget=forms.PasswordInput);
    repeat_new_password = forms.CharField(widget=forms.PasswordInput);
    protection = forms.CharField(label="", widget=forms.HiddenInput(), initial="", required=False);
            
    class Meta:
        model = User;
        fields = ['password'];
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
            
    def clean_password(self):
        password = self.cleaned_data.get('password');
        if (not User.objects.get(username=self.user).check_password(password)):
            raise forms.ValidationError('The password you inputted does not match your current password.');
        return password;    
            
    def clean_new_password(self):
        password = self.cleaned_data.get('new_password');
        if (len(password) < 9):
            raise forms.ValidationError('Your password must contain at least 9 characters.');
        if (not re.match(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{9,}$', password)):
            raise forms.ValidationError('Your password must contain at least one uppercase letter, lowercase letter, and number');
        return password;
        
    def clean_repeat_password(self):
        password = self.cleaned_data.get('new_password');
        repeat_password = self.cleaned_data.get('repeat_password');
        if (not repeat_password or password != repeat_password):
            raise forms.ValidationError("Passwords do not match");
        return repeat_password;
        
    def clean_protection(self):
        if (not self.cleaned_data.get('protection') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
        
class DeactivateAccountForm(forms.ModelForm):
    is_active = forms.BooleanField(initial=False, required=False);
    protection = forms.CharField(label="", widget=forms.HiddenInput(), initial="", required=False);
    
    class Meta:
        model = User;
        fields = ['is_active'];
        
    def clean_protection(self):
        if (not self.cleaned_data.get('protection') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
