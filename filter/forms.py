from django import forms;
from .models import PledgeFilter, WorkerFilter

class PledgeFilterForm(forms.ModelForm):
    not_been_active_in_the_last_n_days = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'filter', 'size' : '2'}), min_value=0);
    paid_at_least_n_times = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'filter', 'size' : '2'}), min_value=0);
    paid_at_least_n_amount_in_total = forms.FloatField(widget=forms.TextInput(attrs={'class' : 'filter', 'size' : '2'}), min_value=0);

    class Meta:
        model = PledgeFilter;
        exclude = ['user',];
        
class WorkerFilterForm(forms.ModelForm):
    not_been_active_in_the_last_n_days = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'filter', 'size' : '2'}), min_value=0);
    
    class Meta: 
        model = WorkerFilter;
        exclude = ['user',];