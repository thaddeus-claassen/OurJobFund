from annoying.functions import get_object_or_None;
from job.models import Job;
from .models import Work, MiscPay, Pledge;
from django import forms;
from datetime import datetime;

class PledgeForm(forms.Form):
    amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '$0.00'}));
    comment = forms.CharField(widget=forms.Textarea, max_length=10000, required=False);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);
    
    class Meta:
        model = Pledge;
        fields = ['amount', 'comment'];
    
    
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
    
class WorkForm(forms.Form):
    payment_type = forms.ChoiceField(choices=(('', '((Please Select your method of receiving payments))'), ('Credit/Debit', 'Credit/Debit'), ('Any', 'Any'), ('Contact Me', 'Contact Me')), required=True);
    expected_finish_date = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}), max_length=100, required=True);
    minimum_amount_requesting = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '$0.00'}), max_length=100, required=True);
    comment = forms.CharField(widget=forms.Textarea, max_length=10000, required=False);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);
    
    class Meta:
        model = Work;
        fields = ['payment_type', 'expected_finish_date', 'minimum_amount_requesting', 'comment'];
    
    def clean_payment_type(self):
        payment_type = self.cleaned_data.get('payment_type');
        if (not payment_type in ['Credit/Debit', 'Any', 'Contact Me']):
            raise forms.ValidationError("Your payment type was not valid.");
        return payment_type;
        
    def clean_expected_finish_date(self):
        date = self.cleaned_data.get('expected_finish_date');
        if (re.match(r'^\d{2}/\d{2}/\d{4}$', date)):
            try:
                date = datetime(month=int(date.split('/')[0]), day=int(date.split('/')[1]), year=int(date.split('/')[2]));
            except ValueError:
                raise forms.ValidationError('Date incorrect.');
        else:
            raise forms.ValidationError("The date must be written in the form 'MM/DD/YYYY'");
        return date;
        
    def clean_minimum_amount_requesting(self):
        money = self.cleaned_data.get('minimum_amount_requesting');
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