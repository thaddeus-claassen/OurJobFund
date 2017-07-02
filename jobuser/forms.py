from django.contrib.auth.models import User;
from .models import Update;
from django import forms;

class UpdateForm(forms.ModelForm):
    title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'placeholder': '(Required)'}), max_length=100);
    images = forms.ImageField(label="Images:", widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False);
    description = forms.CharField(label="Description:", widget=forms.Textarea(attrs={'placeholder': '(Required)'}), max_length=10000);
    
    class Meta: 
        model = Update;
        fields = ['title', 'images', 'description'];
        