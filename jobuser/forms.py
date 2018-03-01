from django import forms;
from .models import JobUser;
import re;

class PledgeForm(forms.Form):
    amount = forms.CharField(label="Pledge:", widget=forms.TextInput(attrs={'placeholder': '$0.00'}));
    description = forms.CharField(label="Description:", widget=forms.Textarea, max_length=10000, required=False);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);
    
    def clean_amount(self):
        pledge = self.cleaned_data.get('amount');
        if (checkStringIsValidMoney(pledge)):
            if (float(pledge) < 0.5):
                raise forms.ValidationError('You cannot pledge less than $0.00.'); 
        else:
            raise forms.ValidationError('Please enter a valid dollar amount.');
        return pledge;
        
    def clean_honey_pot(self):
        if (not self.cleaned_data.get('honey_pot') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
    
class WorkForm(forms.Form):
    type = forms.ChoiceField(label="Type:", choices=(('Working', 'Work'),('Finished Working', 'Finish Working'), ('Finished Accepting Payments', 'Finish Accepting Payment')));
    description = forms.CharField(label="Description:", widget=forms.Textarea, max_length=10000, required=False);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);
    
    def clean_amount(self):
        money = self.cleaned_data.get('amount');
        if (money == ''):
            money = '0';
        if (checkStringIsValidMoney(money)):
            if (float(money) < 0):
                raise forms.ValidationError('You cannot request less than $0.00.'); 
        else:
            raise forms.ValidationError('Please enter a valid dollar amount.');
        return money;
        
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