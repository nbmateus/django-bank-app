from django.db import models
from login.models import User

# Create your models here.
class Account(models.Model):
    code = models.AutoField(primary_key=True)
    users = models.ManyToManyField(User)
    dollarBalance = models.DecimalField(decimal_places=2, max_digits=100, default=0)
    euBalance = models.DecimalField(decimal_places=2, max_digits=100, default=0)
    pesoArBalance = models.DecimalField(decimal_places=2, max_digits=100, default=0)

    def __str__(self):
        return str(self.code)


class Transaction(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='TransactionUser')
    senderAcc = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='senderAcc')
    receiverAcc = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiverAcc')
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    currency = models.CharField(max_length=3 ,choices=(('AR$','AR$'),('US$','US$'),('EU$','EU$'),))
    message = models.CharField(max_length=250)
    


class ActionsLog(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actionLogUser')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    actionType = models.CharField(max_length=25, choices=(('Deposito','Deposito'),('Extraccion','Extraccion'),('Transferencia','Transferencia'),('Creacion|Deposito inicial','Creacion|Deposito inicial'),))
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    currency = models.CharField(max_length=3, choices=(('AR$','AR$'),('US$','US$'),('EU$','EU$'),))




