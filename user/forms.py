from django.contrib.auth.models import User;
from user.models import UserProfile, STATES;
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
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder' : 'First Name'}));
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder' : 'Last Name'}));
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder' : 'Email'}));
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}));
    repeat_password = forms.CharField(label='Repeat Password:', widget=forms.PasswordInput(attrs={'placeholder' : 'Repeat Password'}));
    age_checkbox = forms.BooleanField(label='Check here to verify you are at least 13 years old:');
    
    class Meta: 
        model = User;
        fields = ['first_name', 'last_name', 'email', 'password'];
        
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name');
        if (len(first_name) > 30):
            raise forms.ValidationError('Your first name must not exceed 30 characters.');
        if (not re.match(r'^[A-Za-z]{1,30}$', first_name)):
            raise forms.ValidationError('Your first name may only include alphabetic characters.');
        return first_name;

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name');
        if (len(last_name) > 30):
            raise forms.ValidationError('Your last name must not exceed 30 characters.');
        if (not re.match(r'^[A-Za-z]{1,30}$', last_name)):
            raise forms.ValidationError('Your first name may only include alphabetic characters.');
        return last_name;    
        
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
            
class ChangeNameForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False);
    last_name = forms.CharField(max_length=30, required=False);

    class Meta: 
        model = User;
        fields = ['first_name', 'last_name'];
        
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name');
        if (len(first_name) > 30):
            raise forms.ValidationError('Your first name must not exceed 30 characters.');
        if (not re.match(r'^[A-Za-z]{1,30}$', first_name)):
            raise forms.ValidationError('Your first name may only include alhabetic characters.');
        return first_name;

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name');
        if (len(last_name) > 30):
            raise forms.ValidationError('Your last name must not exceed 30 characters.');
        if (not re.match(r'^[A-Za-z]{1,30}$', last_name)):
            raise forms.ValidationError('Your first name may only include alphabetic characters.');
        return last_name;    
        
class ChangeEmailForm(forms.ModelForm):
    email = forms.CharField(max_length=30, required=False);
    
    class Meta:
        model = User;
        fields = ['email'];
        
    def clean_email(self):
        email = self.cleaned_data.get('email');
        if (User.objects.filter(email=email).exists()):
            raise forms.ValidationError('A user already has that email');
        return email;
            
class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(label="Current Password", widget=forms.PasswordInput);
    new_password = forms.CharField(widget=forms.PasswordInput);
    repeat_new_password = forms.CharField(widget=forms.PasswordInput);
            
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
        
class DeactivateAccountForm(forms.ModelForm):
    is_active = forms.BooleanField(initial=False, required=False);
    
    class Meta:
        model = User;
        fields = ['is_active'];
        
class EditDescriptionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder' : 'This is where you add contact information, social media accounts, and any other information you would like others to know about you'}));

    class Meta:
        model = UserProfile;
        fields = ['description'];
        
class EditInfoForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput(), required=False);
    state = forms.CharField(widget=forms.Select(choices=STATES), required=False);
    occupation = forms.CharField(widget=forms.TextInput(), required=False);
        
    class Meta:
        model = UserProfile;
        fields = ['city', 'state', 'occupation'];
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
