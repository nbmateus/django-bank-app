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
    senderAcc = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='senderAcc')
    receiverAcc = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiverAcc')
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    currency = models.CharField(max_length=3 ,choices=(('AR$','AR$'),('US$','US$'),('EU$','EU$'),))
    message = models.CharField(max_length=250)
    


class ActionsLog(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    actionType = models.CharField(max_length=1, choices=(('D','Deposito'),('E','Extraccion'),('T','Transferencia'),('C','Creacion|Deposito inicial'),))
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    currency = models.CharField(max_length=3, choices=(('AR$','AR$'),('US$','US$'),('EU$','EU$'),))




