from django.urls import path
from bankAccounts.views import createAccount, makeTransaction

urlpatterns = [
    path('createAccount/', createAccount),
    path('makeTransaction/', makeTransaction),
]