from django import forms;
from .models import Job;
from ckeditor.widgets import CKEditorWidget;

class NewJobForm(forms.ModelForm):
    name = forms.CharField(label="Job Title:", max_length=100);
    latitude = forms.FloatField(initial=None);
    longitude = forms.FloatField(initial=None);
    tags = forms.CharField(label="Tags:", max_length=1000);
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False);
    description = forms.CharField(label="Description:", widget=CKEditorWidget(), max_length=10000);

    class Meta: 
        model = Job;
        fields = ['name','latitude', 'longitude', 'tags', 'description'];


    
    
    