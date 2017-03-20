from django.contrib.auth.models import User;
from .models import WorkJobUpdate, Comment;
from django import forms;
from ckeditor.widgets import CKEditorWidget;


class NewWorkJobUpdate(forms.ModelForm):
    title = forms.CharField(label='Title:', max_length=100);
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False);
    description = forms.CharField(label='Description:', widget=CKEditorWidget());
    
    class Meta:
        model = WorkJobUpdate;
        fields = ['title', 'description'];
        
class NewComment(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False);
    comment = forms.CharField(label='Comment:', widget=forms.Textarea);
    
    class Meta:
        model = Comment;
        fields = ['comment'];