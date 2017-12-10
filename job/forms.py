from django import forms;
from .models import Job;
import re;

class NewJobForm(forms.ModelForm):
    name = forms.CharField(label="Job Title:", widget=forms.TextInput(attrs={'placeholder': '(Required)'}), max_length=100);
    location = forms.CharField(label="Location:", widget=forms.TextInput(attrs={'placeholder': '(Optional)'}), max_length=1000, required=False);
    latitude = forms.FloatField(widget=forms.HiddenInput(), initial=None, required=False);
    longitude = forms.FloatField(widget=forms.HiddenInput(), initial=None, required=False);
    tags = forms.CharField(label="Tags:", widget=forms.TextInput(attrs={'placeholder': '(Optional, separated by spaces, alphanumeric characters or "_" only)'}), max_length=1000, required=False);
    image_set = forms.ImageField(label="Images:", widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False);
    description = forms.CharField(label="Description:", widget=forms.Textarea(attrs={'placeholder': '(Required)'}), max_length=10000);
    protection = forms.CharField(label="", widget=forms.HiddenInput(), initial="", required=False);

    class Meta: 
        model = Job;
        fields = ['name', 'location', 'latitude', 'longitude', 'tags', 'image_set', 'description'];
    
    def clean_protection(self):
        if (not self.cleaned_data.get('protection') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";    
    