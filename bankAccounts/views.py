from django.shortcuts import render, redirect
from .forms import AccountForm, TransactionForm, DepositForm, ExtractionForm
from .models import Account, Transaction, ActionsLog
from django.http import JsonResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return render(request, template_name = 'bankAccounts/admin.html', context={'accForm':AccountForm(user=request.user), 'transactionForm':TransactionForm(user=request.user),'depositForm':DepositForm(user=request.user), 'extractionForm':ExtractionForm(user=request.user)})
        return render(request, 'bankAccounts/user.html', {'transactionForm':TransactionForm(user=request.user),'depositForm':DepositForm(user=request.user), 'extractionForm':ExtractionForm(user=request.user)})
    return redirect('/login')


def createAccount(request):
    accForm = AccountForm(request.POST, user=request.user)
    response = {"redirectUrl":"/"}
    if accForm.is_valid():
        accForm.save()
        return JsonResponse(response)
    
    response['errors'] = accForm.errors
    return JsonResponse(response)


def makeTransaction(request):
    transactionForm = TransactionForm(request.POST, user=request.user)
    response = {"redirectUrl":"/"}
    if transactionForm.is_valid():
        transactionForm.save()
        return JsonResponse(response)
    response['errors'] = transactionForm.errors
    return JsonResponse(response)

def deposit(request):
    depositForm = DepositForm(request.POST, user=request.user)
    response = {'message':'Deposito realizado con exito.'}
    if depositForm.is_valid():
        depositForm.save()
        return JsonResponse(response)
    
    response['errors'] = depositForm.errors
    return JsonResponse(response)

def extraction(request):
    depositForm = ExtractionForm(request.POST, user=request.user)
    response = {'message':'Extraccion realizada con exito.'}
    if depositForm.is_valid():
        depositForm.save()
        return JsonResponse(response)
    
    response['errors'] = depositForm.errors
    return JsonResponse(response)

class AccountList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Account
    template_name = 'bankAccounts/accountList.html'

    def get_queryset(self):
        return Account.objects.filter(users__email = self.request.user.email)

class TransactionList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Transaction
    template_name = 'bankAccounts/transactionList.html'

    def get_queryset(self): 
        return Transaction.objects.filter(senderAcc__in=Account.objects.filter(users__email = self.request.user.email))

class AccountTransactionList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Transaction
    template_name = 'bankAccounts/accountTransactionList.html'

    def get_queryset(self):
        account = Account.objects.get(code=self.kwargs['acc_id'])
        if account and account in Account.objects.filter(users__email = self.request.user.email):
            return Transaction.objects.filter(senderAcc=Account.objects.get(code=self.kwargs['acc_id']))
        else:
            return handler404(self.request, "page not found")

class ActionsLogList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = ActionsLog
    template_name = 'bankAccounts/actionsLogList.html'

    def get_queryset(self):
        return ActionsLog.objects.filter(account__in=Account.objects.filter(users__email=self.request.user.email))

class AccountActionsLogList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = ActionsLog
    template_name = 'bankAccounts/accountActionsLogList.html'

    def get_queryset(self):
        account = Account.objects.get(code=self.kwargs['acc_id'])
        if account and account in Account.objects.filter(users__email = self.request.user.email):
            return ActionsLog.objects.filter(account=Account.objects.get(code=self.kwargs['acc_id']))
        else:
            return handler404(self.request, "page not found")


def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
"""


pageNotFound

"""