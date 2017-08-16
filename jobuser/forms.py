from django.contrib.auth.models import User;
from .models import Update, Pledge;
from django import forms;
import re;

class UpdateForm(forms.ModelForm):
    title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'placeholder': '(Required)'}), max_length=100);
    images = forms.ImageField(label="Images:", widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False);
    description = forms.CharField(label="Description:", widget=forms.Textarea(attrs={'placeholder': '(Required)'}), max_length=10000);
    
    class Meta: 
        model = Update;
        fields = ['title', 'images', 'description'];
        
    def clean_title(self):
        title = self.cleaned_data.get('title');
        if (len(title) > 100):
            raise forms.ValidationError('Your title cannot exceed 30 characters in length.');
        if (not re.match(r'^[A-Za-z]{1,30}$', title)):
            raise forms.ValidationError('Your title may only include alphabetic characters or numbers.');
        return title;
        
    def clean_description(self):
        description = self.cleaned_data.get('description');
        if (len(description) > 10000):
            raise forms.ValidationError('Your description cannot be longer than 10000 character in length');
        return description;
        
class PledgeForm(forms.ModelForm):
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '0'}));

    class Meta:
        model = Pledge;
        fields = ['amount'];
        
    def clean_amount(self):
        amount = self.cleaned_data.get('amount');
        print(amount)
        if (not re.match(r'^[0-9]+$', str(amount))):
            raise forms.ValidationError('Only numbers allowed.');
        if (amount == 0):
            raise forms.ValidationError("You cannot pledge $0. That's nonsense.");
        if (len(str(amount)) > 9):
            raise forms.ValidationError("You cannot pledge more than $999,999,999");
        return amount;
        

        