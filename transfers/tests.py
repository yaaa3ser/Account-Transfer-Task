from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from .models import Account
from .forms import TransferForm
from django.db import transaction
from django.db.utils import IntegrityError


class AccountModelTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(
            name="Test Account",
            balance=Decimal('1000.00')
        )

    def test_account_creation(self):
        self.assertTrue(isinstance(self.account, Account))
        self.assertEqual(self.account.__str__(), "Test Account - 1000.00")

    def test_slug_generation(self):
        self.assertTrue(self.account.slug)
        self.assertTrue(self.account.slug.startswith('test-account'))

    

class AccountViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.account1 = Account.objects.create(
            name="Account 1",
            balance=Decimal('1000.00')
        )
        self.account2 = Account.objects.create(
            name="Account 2",
            balance=Decimal('500.00')
        )

    def test_list_accounts_view(self):
        response = self.client.get(reverse('list_accounts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Account 1")
        self.assertContains(response, "Account 2")

    def test_account_detail_view(self):
        response = self.client.get(reverse('account_info', kwargs={'slug': self.account1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Account 1")

    def test_transfer_funds_view(self):
        form_data = {
            'from_account': self.account1.id,
            'to_account': self.account2.id,
            'amount': '100.00'
        }
        response = self.client.post(reverse('transfer_funds'), data=form_data)
        self.assertRedirects(response, reverse('list_accounts'))
        
        # Refresh account instances from database
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        
        self.assertEqual(self.account1.balance, Decimal('900.00'))
        self.assertEqual(self.account2.balance, Decimal('600.00'))
    
    def test_transfer_to_same_account(self):
        form_data = {
            'from_account': self.account1.id,
            'to_account': self.account1.id,
            'amount': '100.00'
        }
        response = self.client.post(reverse('transfer_funds'), data=form_data)
        self.assertEqual(response.status_code, 400)  # Expecting a BadRequest response
        self.assertContains(response, "Cannot transfer funds to the same account.", status_code=400)
    
    def test_insufficient_funds(self):
        form_data = {
            'from_account': self.account1.id,
            'to_account': self.account2.id,
            'amount': '10000.00'
        }
        response = self.client.post(reverse('transfer_funds'), data=form_data)
        self.assertEqual(response.status_code, 400)  # Expecting a BadRequest response
        # The 2 accounts should not have been updated
        self.assertEqual(self.account1.balance, Decimal('1000.00'))
        self.assertEqual(self.account2.balance, Decimal('500.00'))

class TransferFormTest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create(
            name="Account 1",
            balance=Decimal('1000.00')
        )
        self.account2 = Account.objects.create(
            name="Account 2",
            balance=Decimal('500.00')
        )

    def test_invalid_form_missing_data(self):
        form_data = {
            'from_account': self.account1.id,
            'to_account': self.account2.id,
            # 'amount' is missing
        }
        form = TransferForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)

    def test_invalid_form_negative_amount(self):
        form_data = {
            'from_account': self.account1.id,
            'to_account': self.account2.id,
            'amount': '-100.00'
        }
        form = TransferForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)