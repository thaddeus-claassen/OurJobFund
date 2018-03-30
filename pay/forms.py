from annoying.functions import get_object_or_None;
from job.models import Job;
from .models import Pay;
from django import forms;

class PayForm(forms.Form):
    job = forms.ChoiceField();
    amount = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '$0.00'}), required=True);
    type = forms.ChoiceField();
    honey_pot = forms.CharField(label="", widget=forms.HiddenInput, initial="", required=False);
    
    def __init__(self, sender, receiver, *args, **kwargs):
        super(PayForm, self).__init__(*args, **kwargs);
        self.init_job(sender=sender, receiver=receiver);
        self.init_type(receiver=receiver);
        
    def init_job(self, sender, receiver):
        receiver_jobs = Job.objects.none();
        sender_jobs = Job.objects.none();
        for jb in receiver.jobuser_set.all():
            receiver_jobs = receiver_jobs | Job.objects.filter(pk=jb.job.id);
        for jb in sender.jobuser_set.all():
            sender_jobs = sender_jobs | Job.objects.filter(pk=jb.job.id);
        jobs = receiver_jobs & sender_jobs;
        self.jobs = jobs;
        choices = (('', ''),);
        for job in jobs:
            choices = choices + ((job.name, job.name),);
        self.fields['job'] = forms.ChoiceField(choices=choices, required=True);
        
    def init_type(self, receiver):
        if (receiver.profile.stripe_account_id == ''):
            self.fields['type'] = forms.ChoiceField(choices=(('', ''),('Other', 'Other')), required=True);
        else:
            self.fields['type'] = forms.ChoiceField(choices=(('', ''),('Credit/Debit', 'Credit/Debit'),('Other', 'Other')), required=True);
            
    def clean_job(self):
        job = get_object_or_None(Job, name=self.cleaned_data('job'));
        if (job == ''):
            raise forms.ValidationError('Please choose a job.');
        elif (not job in  self.jobs):
            raise forms.ValidationError('Please choose a valid job.');
        return job;
    
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