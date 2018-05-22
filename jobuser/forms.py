from annoying.functions import get_object_or_None;
from job.models import Job;
from django.db.models import Q;
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
        
class PaymentReceivedForm(forms.Form):
    received_payment_from = forms.ChoiceField();
    amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '$0.00'}), required=True);
    comment = forms.CharField(widget=forms.Textarea, max_length=10000, required=False);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);
    
    def __init__(self, jobuser, *args, **kwargs):
        super(PaymentReceivedForm, self).__init__(*args, **kwargs);
        self.jobuser = jobuser;
        pledges = Pledge.objects.filter(Q(jobuser__job=jobuser.job) & ~Q(jobuser__user__username__exact=jobuser.user.username));
        choices = list(set((('', '(Please select a person)'),) + tuple((p.jobuser.user.pk, p.jobuser.user.username) for p in pledges)));
        self.fields['received_payment_from'] = forms.ChoiceField(choices=choices);

    def clean_pay_from(self):
        received_payment_from = int(self.cleaned_data.get('received_payment_from'));
        pledges = Pledge.objects.filter(jobuser__job=self.jobuser.job);
        if (not received_payment_from in [ p.jobuser.user.pk for p in pledges ]):
            raise forms.ValidationError('Invalid Option Selected');
        return received_payment_from;
        
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
        
class StripePaymentForm(forms.Form):
    job = forms.ChoiceField();
    amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '$0.00'}), required=True);
    comment = forms.CharField(widget=forms.Textarea, max_length=10000, required=False);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);
    
    def __init__(self, receiver, *args, **kwargs):
        super(StripePaymentForm, self).__init__(*args, **kwargs);
        jobs = receiver.jobuser_set.filter(~Q(work_status=''));
        choices = (('', '(Please select a job)'),) + tuple((j.job.random_string, j.job.title) for j in jobs);
        self.fields['job'] = forms.ChoiceField(choices=choices);

    def clean_job(self):
        job_random_string = int(self.cleaned_data.get('job_random_string'));
        jobs = receiver.jobuser_set.filter(~Q(work_status=''));
        if (not job_random_string in [ j.job.ranom_string for j in jobs ]):
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
    #payment_type = forms.ChoiceField(choices=(('', '(Please Select your method of receiving payments)'), ('Credit/Debit', 'Credit/Debit'), ('Either', 'Either'), ('Contact Me', 'Contact Me')), required=True);
    comment = forms.CharField(widget=forms.Textarea, max_length=10000, required=False);
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);
    
    class Meta:
        model = Work;
        fields = ['payment_type'];

    #def clean_payment_type(self):
    #    payment_type = self.cleaned_data.get('payment_type');
    #    if (not payment_type in ['Credit/Debit', 'Any', 'Contact Me']):
    #        raise forms.ValidationError("Your payment type was not valid.");
    #    return payment_type;

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