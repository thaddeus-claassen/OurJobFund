from django import forms;
from .models import Update;
import re;

TYPES = (('Comment', 'Comment'), ('Working', 'Working'), ('Finished', 'Finished'), ('Pledge', 'Pledge'), ('Pay', 'Pay'));

class UpdateForm(forms.Form):
    type = forms.ChoiceField(label="Type:", choices=TYPES);
    amount = forms.FloatField(label='Amount:', widget=forms.TextInput(attrs={'placeholder' : '$0.00'}));
    pay_to = forms.ChoiceField();
    title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'placeholder': '(Required)'}), max_length=100);
    images = forms.ImageField(label="Images:", widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False);
    description = forms.CharField(label="Description:", widget=forms.Textarea(), required=False, max_length=10000);
    protection = forms.CharField(label="", widget=forms.HiddenInput(), initial="", required=False);
    
    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(args, kwargs);
        receivers = [('@@@', '')];
        if (len(args) == 0):
            receivers =  receivers + [(j.user.pk, j.user.username) for j in kwargs['job'].jobuser_set.all().exclude(user__id=kwargs['user'].pk)];
        else:
            receivers = receivers + [(args[0]['pay_to'], '')];
        self.fields['pay_to'] = forms.ChoiceField(
            label='Pay To:',
            choices=receivers,
        );

        
    def clean_protection(self):
        if (not self.cleaned_data.get('protection') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
        