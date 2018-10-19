from annoying.functions import get_object_or_None;
from job.models import Job;
from django.db.models import Q;
from datetime import datetime;
from .models import Work, StripePay, MiscPay, Pledge;
from django import forms;

class PledgeForm(forms.Form):
    amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '$0.00'}));
    comment = forms.CharField(widget=forms.Textarea, max_length=10000, required=False);
    #This is honey pot
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'make-this-disappear'}), initial="", required=False);

    class Meta:
        model = Pledge;
        fields = ['amount', 'comment'];

    def clean_amount(self):
        pledge = self.cleaned_data.get('amount');
        if (checkStringIsValidMoney(pledge)):
            if (float(pledge) < 0.5):
                raise forms.ValidationError('You cannot pledge less than $0.50.'); 
        else:
            raise forms.ValidationError('Please enter a valid dollar amount.');
        return pledge;

    def clean_username(self):
        if (not self.cleaned_data.get('username') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";

class StripePayForm(forms.Form):
    amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '$0.00'}), required=True);
    comment = forms.CharField(widget=forms.Textarea, max_length=10000, required=False);
    #This is honey pot
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'make-this-disappear'}), initial="", required=False);
    
    #def __init__(self, *args, **kwargs):
    #    super(StripePayForm, self).__init__(*args, **kwargs);
    
    class Meta:
        model = StripePay;
        fields = ['amount', 'comment', 'username'];
    
    def clean_amount(self):
        pay = self.cleaned_data.get('amount');
        if (checkStringIsValidMoney(pay)):
            if (float(pay) == 0):
                raise forms.ValidationError('$0.00 is invalid.');
        else:
            raise forms.ValidationError('Please enter a valid dollar amount.');
        return pay;
        
    def clean_username(self):
        if (not self.cleaned_data.get('username') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
        
class MiscPayForm(forms.Form):
    receiver = None;
    amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '$0.00'}), required=True);
    comment = forms.CharField(widget=forms.Textarea, max_length=10000, required=False);
    #This is honey pot
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'make-this-disappear'}), initial="", required=False);
    
    class Meta:
        model = MiscPay;
        fields = ['receiver','amount', 'comment', 'username'];
        
    def __init__(self, *args, **kwargs):
        job = kwargs.pop('job', None);
        super(MiscPayForm, self).__init__(*args, **kwargs);
        workers = job.jobuser_set.filter(~Q(work_status=''));
        choices = [ (w.user.username, w.user.username) for w in workers ]
        self.fields['receiver'] = forms.ChoiceField(choices = choices);
    
    def clean_receiver(self):
        receiver = self.cleaned_data.get('receiver');
        if ((receiver, receiver) not in self.fields['receiver'].choices):
            raise forms.ValidationError('You cannot pay that person.');
        return receiver;
    
    def clean_amount(self):
        pay = self.cleaned_data.get('amount');
        if (checkStringIsValidMoney(pay)):
            if (float(pay) == 0):
                raise forms.ValidationError('$0.00 is invalid.');
        else:
            raise forms.ValidationError('Please enter a valid dollar amount.');
        return pay;
        
    def clean_username(self):
        if (not self.cleaned_data.get('username') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";
    
class WorkForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, max_length=10000, required=False);
    #This is honey pot
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'make-this-disappear'}), initial="", required=False);
    
    class Meta:
        model = Work;
        fields = ['payment_type'];

    def clean_username(self):
        if (not self.cleaned_data.get('username') == ""):
            raise forms.ValidationError('It seems you are a bot.');
        return "";

class FinishForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, max_length=10000, required=False);
    #This is honey pot
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'make-this-disappear'}), initial="", required=False);
    
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