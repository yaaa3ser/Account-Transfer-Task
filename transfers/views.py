from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView
from django.db import transaction
from django.http import HttpResponseBadRequest

from .models import Account
from .forms import TransferForm

from io import StringIO
import csv


class ImportAccountsView(View):
    template_name = 'accounts/import_accounts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            return HttpResponseBadRequest("No file uploaded.")

        data = csv_file.read().decode('utf-8')
        file = StringIO(data)
        reader = csv.reader(file)
        next(reader)  # Skip first row --> header
        
        # either all rows are successfully imported or none
        with transaction.atomic():
            for row in reader:
                if Account.objects.filter(id=row[0]).exists():
                    continue
                Account.objects.create(
                    id=row[0],
                    name=row[1],
                    balance=row[2]
                )
        return redirect('list_accounts')


class ListAccountsView(TemplateView):
    template_name = 'accounts/list_accounts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = Account.objects.all()
        return context


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
