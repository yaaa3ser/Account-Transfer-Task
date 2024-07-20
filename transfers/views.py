from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView, ListView
from django.db import transaction
from django.http import HttpResponseBadRequest
from .utils import import_accounts_from_file

from .models import Account
from .forms import TransferForm

from io import StringIO
import csv


class ImportAccountsView(View):
    template_name = 'accounts/import_accounts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        generic_file = request.FILES.get('file')
        if not generic_file:
            return HttpResponseBadRequest("No file uploaded.")

        records = import_accounts_from_file(generic_file)
        
        # either all rows are successfully imported or none
        with transaction.atomic():
            for row in records:
                if isinstance(row, list):
                    # Handle CSV format
                    account_id, name, balance = row
                elif isinstance(row, dict):
                    # Handle JSON or XML format
                    account_id = row['ID']
                    name = row['Name']
                    balance = row['Balance']
                if Account.objects.filter(id=account_id).exists():
                    continue
                Account.objects.create(
                    id=account_id,
                    name=name,
                    balance=balance
                )
        return redirect('list_accounts')


class ListAccountsView(ListView):
    model = Account
    template_name = 'accounts/list_accounts.html'
    context_object_name = 'accounts'
    paginate_by = 10


class AccountDetailView(DetailView):
    model = Account
    template_name = 'accounts/account_info.html'
    context_object_name = 'account'
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Account, slug=slug)


class TransferFundsView(FormView):
    template_name = 'transfers/transfer_funds.html'
    form_class = TransferForm

    def form_valid(self, form):
        from_account = form.cleaned_data['from_account']
        to_account = form.cleaned_data['to_account']
        amount = form.cleaned_data['amount']
        
        if from_account == to_account:
            return HttpResponseBadRequest("Cannot transfer funds to the same account.")
        
        if from_account.balance < amount:
            return HttpResponseBadRequest("You do not have enough funds to transfer.")
        
        with transaction.atomic():
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
        
        return redirect('list_accounts')
