from django import forms;
from .models import Job;
from annoying.functions import get_object_or_None;
import re;

class NewJobForm(forms.ModelForm):
    public = forms.ChoiceField(label="Type", choices=(("True", "Public"),("False", "Private")));
    title = forms.CharField(max_length=100);
    formatted_location = forms.CharField(label="", widget=forms.HiddenInput(), initial=None, required=False);
    location = forms.CharField(widget=forms.TextInput, max_length=1000, required=False);
    latitude = forms.FloatField(widget=forms.HiddenInput(), initial=None, required=False);
    longitude = forms.FloatField(widget=forms.HiddenInput(), initial=None, required=False);
    tags = forms.CharField(widget=forms.TextInput, max_length=1000, required=False);
    image_set = forms.ImageField(label="Images", widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False);
    comment = forms.CharField(widget=forms.Textarea, max_length=10000);
    #This is honey pot
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'make-this-disappear'}), initial="", required=False);

    class Meta:
        model = Job;
        fields = ['public', 'title', 'formatted_location', 'location', 'latitude', 'longitude', 'tags', 'image_set', 'comment'];
    
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
    
    def clean_username(self):
        if (not self.cleaned_data.get('username') == ""):
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