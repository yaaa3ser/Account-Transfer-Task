from django.urls import path
from .views import ImportAccountsView, ListAccountsView, AccountDetailView, TransferFundsView

urlpatterns = [
    path('import/', ImportAccountsView.as_view(), name='import_accounts'),
    path('', ListAccountsView.as_view(), name='list_accounts'),
    path('transfer/', TransferFundsView.as_view(), name='transfer_funds'),
    path('<slug:slug>/', AccountDetailView.as_view(), name='account_info'),
]
