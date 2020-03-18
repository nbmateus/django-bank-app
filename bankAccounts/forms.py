from django import forms
from .models import Account, Transaction, ActionsLog
from login.models import User
from decimal import Decimal

class AccountForm2(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['users','dollarBalance','euBalance', 'pesoArBalance']
        labels = {
            'users':'Propietario/s de la cuenta',
            'dollarBalance':'Dolares (US$)',
            'euBalance':'Euros (EU$)',
            'pesoArBalance':'Pesos (AR$)'}
        
        widgets = {
            'users': forms.SelectMultiple(attrs={'class':'selectpicker', 'data-live-search':'true','title':'Lista de usuarios'}),
            'dollarBalance': forms.NumberInput(attrs={'class':'form-control'}),
            'euBalance': forms.NumberInput(attrs={'class':'form-control', 'min':'0'}),
            'pesoArBalance': forms.NumberInput(attrs={'class':'form-control'})
            }
    
    def clean(self):
        total = self.cleaned_data.get('dollarBalance')+self.cleaned_data.get('euBalance')+self.cleaned_data.get('pesoArBalance')
        if total <= 0:
            raise forms.ValidationError('Para crear la cuenta se debe depositar.')
        return self.cleaned_data

class AccountForm(forms.Form):
    users = forms.ModelMultipleChoiceField(label='Propietario/s de la cuenta', queryset=User.objects.all(), widget=forms.SelectMultiple(attrs={'class':'selectpicker', 'data-live-search':'true','title':'Usuarios'}))
    deposit = forms.DecimalField(label='Deposito inicial', widget=forms.NumberInput(attrs={'class':'form-control', 'min':'0'}))
    currency = forms.ChoiceField(label='Moneda', widget=forms.Select(attrs={'class':'form-control'}), choices=(('AR$','AR$'),('US$','US$'),('EU$','EU$')))

    def save(self):
        account = Account.objects.create()
        account.users.set(self.cleaned_data.get('users'))
        currency = self.cleaned_data.get('currency')
        deposit = self.cleaned_data.get('deposit')

        if currency == 'AR$':
            account.pesoArBalance = deposit

        elif currency == 'US$':
            account.dollarBalance = deposit
        
        elif currency == 'EU$':
            account.euBalance = deposit

        account.save()
        accountLog = ActionsLog(account=account,actionType='C',amount=deposit, currency=currency)
        accountLog.save()
        return account


class TransactionForm(forms.ModelForm):
    #email = forms.EmailField(label='Tu correo electronico', widget=forms.EmailInput(attrs={'class':'form-control'}))
    sAccNumber = forms.IntegerField(label='Numero de cuenta emisora', widget=forms.NumberInput(attrs={'class':'form-control'}))
    rAccNumber = forms.IntegerField(label='Numero de cuenta receptora', widget=forms.NumberInput(attrs={'class':'form-control'}))

    
    class Meta:
        model = Transaction
        fields = ['amount','currency','message']
        labels = {
            'amount':'monto',
            'currency':'moneda',
            'message':'mensaje',
        }
        widgets = {
            'amount':forms.NumberInput(attrs={'class':'form-control','min':'0.1'}),
            'currency':forms.Select(attrs={'class':'form-control'},choices=(('AR$','AR$'),('US$','US$'),('EU$','EU$'))),
            'message':forms.TextInput(attrs={'class':'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        
    def clean_sAccNumber(self):
        try:
            senderAcc = Account.objects.get(code=str(self.cleaned_data.get('sAccNumber')))
        except Exception as e:
            print("Exception: "+str(e))
            senderAcc = None
        print("SENDER ACC: "+str(senderAcc))
        print("USER: "+str(self.user))
        if not senderAcc or (senderAcc and not self.user in senderAcc.users.all()):
            raise forms.ValidationError('El numero de cuenta emisora no existe o no le pertenece a usted.')
        return senderAcc
    
    def clean_rAccNumber(self):
        try:
            receiverAcc = Account.objects.get(code=self.cleaned_data.get('rAccNumber'))
        except Exception as e:
            print("Exception: "+str(e))
            receiverAcc = None
        if not receiverAcc:
            raise forms.ValidationError('El numero de cuenta receptora no existe.')
        return receiverAcc
    
    def clean(self):
        senderAcc = self.clean_sAccNumber()
        if self.cleaned_data.get('currency') == 'AR$':
            senderAccAmount = senderAcc.pesoArBalance
        if self.cleaned_data.get('currency') == 'US$':
            senderAccAmount = senderAcc.dollarBalance
        if self.cleaned_data.get('currency') == 'EU$':
            senderAccAmount = senderAcc.euBalance
        if Decimal(senderAccAmount) < self.cleaned_data.get('amount'):
            raise forms.ValidationError('Tu cuenta no tiene fondos suficientes.')
        return self.cleaned_data
    
    def save(self):
        senderAcc = Account.objects.get(code=str(self.cleaned_data.get('sAccNumber')))
        receiverAcc = Account.objects.get(code=str(self.cleaned_data.get('rAccNumber')))
        transaction = Transaction(
            senderAcc=senderAcc, receiverAcc=receiverAcc,
            amount=self.cleaned_data.get('amount'), currency=self.cleaned_data.get('currency'),
            message=self.cleaned_data.get('message'))
        
        if self.cleaned_data.get('currency') == 'AR$':
            pesoS = Decimal(senderAcc.pesoArBalance)
            pesoR = Decimal(receiverAcc.pesoArBalance)
            pesoS -= self.cleaned_data.get('amount')
            pesoR += self.cleaned_data.get('amount')
            senderAcc.dollarBalance = pesoS
            receiverAcc.dollarBalance = pesoR

        if self.cleaned_data.get('currency') == 'US$':
            dollarS = Decimal(senderAcc.dollarBalance)
            dollarR = Decimal(receiverAcc.dollarBalance)
            dollarS -= self.cleaned_data.get('amount')
            dollarR += self.cleaned_data.get('amount')
            senderAcc.dollarBalance = dollarS
            receiverAcc.dollarBalance = dollarR

        if self.cleaned_data.get('currency') == 'EU$':
            euS = Decimal(senderAcc.euBalance)
            euR = Decimal(receiverAcc.euBalance)
            euS -= self.cleaned_data.get('amount')
            euRe += self.cleaned_data.get('amount')
            senderAcc.dollarBalance = euS
            receiverAcc.dollarBalance = euR

        transaction = transaction.save()
        senderAcc.save()
        receiverAcc.save() 
        senderLog = ActionsLog(account=senderAcc, actionType='T',
             amount=(Decimal(self.cleaned_data.get('amount'))*-1), currency=self.cleaned_data.get('currency'))
        senderLog.save()
        receiverLog = ActionsLog(account=receiverAcc, actionType='T',
             amount=self.cleaned_data.get('amount'), currency=self.cleaned_data.get('currency'))
        receiverLog.save()
        return transaction

    
    
        
        
