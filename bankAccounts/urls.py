from django.urls import path
from bankAccounts.views import(
    createAccount, makeTransaction, AccountList,
     TransactionList, AccountTransactionList, ActionsLogList, AccountActionsLogList, extraction, deposit
) 

# /home/
urlpatterns = [
    path('createAccount/', createAccount),
    path('makeTransaction/', makeTransaction),
    path('deposit/', deposit),
    path('extraction/', extraction),
    path('myAccounts/', AccountList.as_view()),
    path('myTransactions/',TransactionList.as_view()),
    path('transactions/<int:acc_id>/',AccountTransactionList.as_view()),
    path('actionslog/',ActionsLogList.as_view()),
    path('actionslog/<int:acc_id>/',AccountActionsLogList.as_view()),
]