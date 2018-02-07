from django import forms;
from .models import JobUser;
import re;

class PledgeForm(forms.ModelForm):
    amount = forms.FloatField(label="Pledge Amount:", widget=forms.TextInput(attrs={'placeholder' : '$0.00'}), required=True);
    comment = forms.CharField(label="Comment:", widget=forms.Textarea(attrs={'placeholder' : '(Optional)'}), required=False, max_length=10000);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);
        
    class Meta:
        model = JobUser;
        fields = ['amount', 'comment'];
        
    def clean_protection(self):
        if (not self.cleaned_data.get('honey_pot') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
        
class WorkForm(forms.ModelForm):
    
        