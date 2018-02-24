from django import forms;
from .models import Update;
import re;

class UpdateForm(forms.Form):
    images = forms.ImageField(label="Images:", widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False);
    description = forms.CharField(label="Description:", widget=forms.Textarea, max_length=10000, required=False);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);

    def clean_honey_pot(self):
        if (not self.cleaned_data.get('honey_pot') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
        
class PayForm(forms.Form):
    type = forms.ChoiceField(choices=(('Credit', 'Credit'), ('Other', 'Other')), required=True);
    amount = forms.CharField(label="Pay Amount:", widget=forms.TextInput(attrs={'placeholder': '$0.00'}), required=True);
    description = forms.CharField(label="Description:", widget=forms.Textarea, max_length=10000, required=False);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);

    def clean_amount(self):
        pay = self.cleaned_data.get('amount');
        if (checkStringIsValidMoney(pay)):
            if (float(pay) == 0):
                raise forms.ValidationError('$0.00 is invalid.'); 
        else:
            raise forms.ValidationError('Please enter a valid dollar amount.');
        return pay;
    
def checkStringIsValidMoney(money):
    valid = False;
    s = money.split('.');
    if (len(s) == 1 and s[0].isdigit()):
        valid = True;
    elif (len(s) == 2 and s[0].isdigit() and (len(s[1]) == 0 or len(s[1]) == 1) and s[1].isdigit()):
        valid = True;
    return valid;
    
    