from django import forms;
from .models import Job, UserWorkerFilter, UserPledgeFilter;

class NewJobForm(forms.ModelForm):
    name = forms.CharField(label="Job Title:", max_length=100);
    latitude = forms.FloatField(initial=None);
    longitude = forms.FloatField(initial=None);
    tags = forms.CharField(label="Tags:", max_length=1000);
    description = forms.CharField(label="Description:", widget=forms.Textarea, max_length=10000);

    class Meta: 
        model = Job;
        fields = ['name','latitude', 'longitude', 'tags', 'description'];
        
        
CHOICES = [('day', 'days'), ('week', 'weeks'), ('month', 'months'), ('year', 'years')];
 
class ApplyPledgeMetricsForm(forms.ModelForm):
    inactive = forms.IntegerField(label='', min_value=0);
    inactive_unit = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES);
    updated = forms.IntegerField(label='', min_value=0);
    updated_unit = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES);
    completed_fewer = forms.IntegerField(label='', min_value=0);
    failed_to_complete = forms.IntegerField(label='', min_value=0);
    completed_percent = forms.FloatField(label='', min_value=0, max_value=100);
    completed_ratio = forms.FloatField(label='', min_value=.0001);
        
    class Meta:
        model = UserWorkerFilter;
        fields = ['inactive', 'inactive_unit', 'updated', 'updated_unit', 'completed_fewer', 'failed_to_complete', 'completed_percent', 'completed_ratio'];
    
class ApplyWorkMetricsForm(forms.ModelForm):
    inactive = forms.IntegerField(label='', min_value=0);
    inactive_unit = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES);
    failed_to_pay = forms.IntegerField(label='', min_value=0);
    averaged = forms.IntegerField(label='', min_value=0);
    paid_x_times = forms.IntegerField(label='', min_value=0);
    
    class Meta:
        model = UserPledgeFilter;
        fields = ['inactive', 'inactive_unit', 'failed_to_pay', 'averaged', 'paid_x_times'];
    
    
    
    
    
    