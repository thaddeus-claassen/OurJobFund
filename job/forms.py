from django import forms;
from .models import Job;
import re;

class NewJobForm(forms.Form):
    title = forms.CharField(max_length=100);
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : '(Any valid location on Google Maps)'}), max_length=1000, required=False);
    latitude = forms.FloatField(widget=forms.HiddenInput(), initial=None, required=False);
    longitude = forms.FloatField(widget=forms.HiddenInput(), initial=None, required=False);
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '(Optional)'}), max_length=1000, required=False);
    image_set = forms.ImageField(label="Images", widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False);
    description = forms.CharField(max_length=10000);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput(), initial="", required=False);

    class Meta: 
        model = Job;
        fields = ['title', 'location', 'latitude', 'longitude', 'tags', 'image_set', 'description', 'pledge'];
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags');
        if (len(tags) > 0):
            if (not re.match(r'^[A-Za-z0-9\s_]+$', tags)):
                raise forms.ValidationError('Tags can only include alphabetic, numeric or "_" characters, separated by spaces.');
            tagsArray = tags.split();
            for tag in tagsArray:
                if (len(tag) > 30):
                    raise forms.ValidationError('Each tag cannot be more than 30 characters.');
        return tags;
    
    def clean_honey_pot(self):
        if (not self.cleaned_data.get('honey_pot') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
        
def checkStringIsValidMoney(money):
    valid = False;
    s = money.split('.');
    if (len(s) == 1 and s[0].isdigit()):
        valid = True;
    elif (len(s) == 2 and s[0].isdigit() and (len(s[1]) == 0 or len(s[1]) == 1) and s[1].isdigit()):
        valid = True;
    return valid;