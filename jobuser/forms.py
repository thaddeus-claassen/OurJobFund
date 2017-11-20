from .models import Pledge;
from django import forms;
import re;

class PledgeForm(forms.ModelForm):
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '0', 'size': '6'}));

    class Meta:
        model = Pledge;
        fields = ['amount'];
        
    def clean_amount(self):
        amount = self.cleaned_data.get('amount');
        if (not re.match(r'^[0-9]+$', str(amount))):
            raise forms.ValidationError('Only numbers allowed.');
        if (amount == 0):
            raise forms.ValidationError("You cannot pledge $0. That's nonsense.");
        if (len(str(amount)) > 9):
            raise forms.ValidationError("You cannot pledge more than $999,999,999");
        return amount;
        

        