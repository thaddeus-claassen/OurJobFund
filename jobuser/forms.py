from annoying.functions import get_object_or_None;
from job.models import Job;
from datetime import datetime;
from .models import Work, MiscPay, Pledge;
from django import forms;

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
    type = forms.ChoiceField(choices=(('', '(Please Select Payment Method)'), ('Credit/Debit', 'Credit/Debit'), ('Already Paid', 'Already Paid')));
    pay_to = forms.ChoiceField();
    amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '$0.00'}), required=True);
    comment = forms.CharField(widget=forms.Textarea, max_length=10000, required=False);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);
    
    def __init__(self, jobuser, *args, **kwargs):
        super(PayForm, self).__init__(*args, **kwargs);
        self.jobuser = jobuser;
        workers = Work.objects.filter(jobuser__job=jobuser.job);
        choices = (('', '(Please select someone to pay)'),) + tuple((w.jobuser.user.pk, w.jobuser.user.username) for w in workers);
        self.fields['pay_to'] = forms.ChoiceField(choices=choices);

    def clean_type(self):
        type = self.cleaned_data.get('type');
        if (type == ''):
            raise forms.ValidationError('Please select and option.')
        elif (type != 'Credit/Debit' and type != 'Already Paid'):
            raise forms.ValidationError('Invalid Option Selected.');
        return type;

    def clean_pay_to(self):
        pay_to = int(self.cleaned_data.get('pay_to'));
        workers = Work.objects.filter(jobuser__job=self.jobuser.job);
        if (not pay_to in [ w.jobuser.user.pk for w in workers ]):
            raise forms.ValidationError('Invalid Option Selected');
        return pay_to;
        
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
    payment_type = forms.ChoiceField(choices=(('', '(Please Select your method of receiving payments)'), ('Credit/Debit', 'Credit/Debit'), ('Either', 'Either'), ('Contact Me', 'Contact Me')), required=True);
    comment = forms.CharField(widget=forms.Textarea, max_length=10000, required=False);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);
    
    class Meta:
        model = Work;
        fields = ['payment_type'];

    def clean_payment_type(self):
        payment_type = self.cleaned_data.get('payment_type');
        if (not payment_type in ['Credit/Debit', 'Any', 'Contact Me']):
            raise forms.ValidationError("Your payment type was not valid.");
        return payment_type;

    def clean_honey_pot(self):
        if (not self.cleaned_data.get('honey_pot') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";

class FinishForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, max_length=10000, required=False);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);

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