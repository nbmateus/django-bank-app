from django.contrib import admin
from .models import Account, Transaction, ActionsLog

# Register your models here.
admin.site.register(Account)
admin.site.register(ActionsLog)
admin.site.register(Transaction)
