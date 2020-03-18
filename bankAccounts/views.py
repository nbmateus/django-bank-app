from django.shortcuts import render, redirect
from .forms import AccountForm, TransactionForm
from .models import Account, Transaction
from django.http import JsonResponse

# Create your views here.
"""
getAccounts(user)
getTransactions(account)
getLogs(account)

deposit(account, amount, currency)
exctract(account, amount, currency)

transfer(senderAcc, recAcc, ammount, currency, message)
log()

createAccount()

"""

def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return render(request, template_name = 'admin.html', context={'accForm':AccountForm()})
        return render(request, 'user.html', {'transactionForm':TransactionForm(user=request.user)})
    return redirect('/login')


def createAccount(request):
    accForm = AccountForm(request.POST)
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


        