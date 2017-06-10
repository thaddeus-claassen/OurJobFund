from django import forms;
from .models import Job;

class NewJobForm(forms.ModelForm):
    name = forms.CharField(label="Job Title:", widget=forms.TextInput(attrs={'placeholder': '(Required)'}), max_length=100);
    location = forms.CharField(label="Location:", widget=forms.TextInput(attrs={'placeholder': '(Optional)'}), max_length=1000, required=False);
    latitude = forms.FloatField(widget=forms.HiddenInput(), initial=None, required=False);
    longitude = forms.FloatField(widget=forms.HiddenInput(), initial=None, required=False);
    tags = forms.CharField(label="Tags:", widget=forms.TextInput(attrs={'placeholder': '(Optional)'}), max_length=1000);
    images = forms.ImageField(label="Images:", widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False);
    description = forms.CharField(label="Description:", widget=forms.Textarea(attrs={'placeholder': '(Required)'}), max_length=10000);

    class Meta: 
        model = Job;
        fields = ['name','location', 'latitude', 'longitude', 'tags', 'description'];


    
    
    