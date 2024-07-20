from django import forms
from .models import Account

class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all(), label='Transfer from')
    to_account = forms.ModelChoiceField(queryset=Account.objects.all(), label='Transfer to')
    amount = forms.DecimalField(max_digits=12, decimal_places=2)
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

