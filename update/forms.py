from django import forms;
from .models import Update;
import re;


class UpdateForm(forms.ModelForm):
    title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'placeholder': '(Required)'}), max_length=100);
    images = forms.ImageField(label="Images:", widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False);
    description = forms.CharField(label="Description:", widget=forms.Textarea(attrs={'placeholder': '(Required)'}), max_length=10000);
    protection = forms.CharField(label="", widget=forms.HiddenInput(), initial="", required=False);
    
    class Meta: 
        model = Update;
        fields = ['title', 'images', 'description'];
        
    def clean_protection(self):
        if (not self.cleaned_data.get('protection') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";