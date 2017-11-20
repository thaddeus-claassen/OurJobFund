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

    class Meta: 
        model = Job;
        fields = ['name', 'location', 'latitude', 'longitude', 'tags', 'image_set', 'description'];

    def clean_name(self):
        name = self.cleaned_data.get('name');
        if (len(name) > 100):
            raise forms.ValidationError('The name cannot have more than 100 characters.');
        return name;
        
    def clean_tags(self):
        tags = ' '.join(self.cleaned_data.get('tags').split());
        tagsArray = tags.split(" ");
        for tag in tagsArray:
            if (len(tag) > 30):
                raise forms.ValidationError('Each tag must have 30 characters or fewer.');
                break;
            if (not re.match(r'^[A-Za-z0-9_]*$', tag)):
                raise forms.ValidationError('Each tag may only include alphabetic characters, numbers, and "_", separated by spaces.');
        return tags;
    
    
    