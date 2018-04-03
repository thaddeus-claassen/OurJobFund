from annoying.functions import get_object_or_None;
from job.models import Job;
from .models import Pay;
from django import forms;

class PayForm(forms.Form):
    type = forms.ChoiceField();
    amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '$0.00'}), required=True);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);
    
    def __init__(self, sender, receiver, *args, **kwargs):
        super(PayForm, self).__init__(*args, **kwargs);
        self.init_type(receiver=receiver);
        
    def init_type(self, receiver):
        if (receiver.profile.stripe_account_id == ''):
            self.fields['type'] = forms.ChoiceField(choices=(('', '(Please select how you will pay.)'),('Other', 'Negotiate between us.')), required=True);
        else:
            self.fields['type'] = forms.ChoiceField(choices=(('', '(Please select how you will pay.)'),('Credit/Debit', 'Credit/Debit'),('Other', 'Negotiate between us.')), required=True);
    
    def clean_amount(self):
        pay = self.cleaned_data.get('amount');
        if (checkStringIsValidMoney(pay)):
            if (float(pay) == 0):
                raise forms.ValidationError('$0.00 is invalid.');
        else:
            raise forms.ValidationError('Please enter a valid dollar amount.');
        return pay;
        
    def clean_honey_pot(self):
        if (not self.cleaned_data.get('honey_pot') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";