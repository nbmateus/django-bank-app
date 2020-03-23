from django import forms
from .models import Account, Transaction, ActionsLog
from login.models import User
from decimal import Decimal

class AccountForm(forms.Form):
    users = forms.ModelMultipleChoiceField(label='Propietario/s de la cuenta', queryset=User.objects.all(), widget=forms.SelectMultiple(attrs={'class':'selectpicker', 'data-live-search':'true','title':'Usuarios'}))
    deposit = forms.DecimalField(label='Deposito inicial', widget=forms.NumberInput(attrs={'class':'form-control', 'min':'0'}))
    currency = forms.ChoiceField(label='Moneda', widget=forms.Select(attrs={'class':'form-control'}), choices=(('AR$','AR$'),('US$','US$'),('EU$','EU$')))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AccountForm, self).__init__(*args, **kwargs)

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
        accountLog = ActionsLog(user=self.user, account=account,actionType='Creacion|Deposito inicial',amount=deposit, currency=currency)
        accountLog.save()
        return account


class TransactionForm(forms.ModelForm):
    #email = forms.EmailField(label='Tu correo electronico', widget=forms.EmailInput(attrs={'class':'form-control'}))
    #sAccNumber = forms.IntegerField(label='Numero de cuenta emisora', widget=forms.NumberInput(attrs={'class':'form-control'}))
    sAccNumber = forms.ModelChoiceField(label='Numero de cuenta emisora', queryset=Account.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
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
        self.fields['sAccNumber'].queryset = Account.objects.filter(users__email=self.user.email)
        
    """def clean_sAccNumber(self):
        try:
            senderAcc = Account.objects.get(code=str(self.cleaned_data.get('sAccNumber')))
        except Exception as e:
            print("Exception: "+str(e))
            senderAcc = None
        print("SENDER ACC: "+str(senderAcc))
        print("USER: "+str(self.user))
        if not senderAcc or (senderAcc and not self.user in senderAcc.users.all()):
            raise forms.ValidationError('El numero de cuenta emisora no existe o no le pertenece a usted.')
        return senderAcc"""
    
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
        senderAcc = self.cleaned_data.get('sAccNumber')
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
        senderAcc = self.cleaned_data.get('sAccNumber')
        receiverAcc = Account.objects.get(code=str(self.cleaned_data.get('rAccNumber')))
        transaction = Transaction(user=self.user,
            senderAcc=senderAcc, receiverAcc=receiverAcc,
            amount=self.cleaned_data.get('amount'), currency=self.cleaned_data.get('currency'),
            message=self.cleaned_data.get('message'))
        
        if self.cleaned_data.get('currency') == 'AR$':
            pesoS = Decimal(senderAcc.pesoArBalance)
            pesoR = Decimal(receiverAcc.pesoArBalance)
            pesoS -= self.cleaned_data.get('amount')
            pesoR += self.cleaned_data.get('amount')
            senderAcc.pesoArBalance = pesoS
            receiverAcc.pesoArBalance = pesoR

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
            euR += self.cleaned_data.get('amount')
            senderAcc.euBalance = euS
            receiverAcc.euBalance = euR

        transaction = transaction.save()
        senderAcc.save()
        receiverAcc.save() 
        senderLog = ActionsLog(user=self.user, account=senderAcc, actionType='Transferencia',
             amount=(Decimal(self.cleaned_data.get('amount'))*-1), currency=self.cleaned_data.get('currency'))
        senderLog.save()
        receiverLog = ActionsLog(user=self.user, account=receiverAcc, actionType='Transferencia',
             amount=self.cleaned_data.get('amount'), currency=self.cleaned_data.get('currency'))
        receiverLog.save()
        return transaction

class DepositForm(forms.Form):    
    account = forms.ModelChoiceField(
        label='Numero de cuenta', queryset=Account.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}))

    currency = forms.ChoiceField(
        label='Moneda',choices=(('AR$','AR$'),('US$','US$'),('EU$','EU$')),
        widget=forms.Select(attrs={'class':'form-control'}))
    amount = forms.DecimalField(label='Monto',widget=forms.NumberInput(attrs={'class':'form-control','min':'1'}))


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DepositForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(users__email=self.user.email)
    
    def save(self, commit=False):
        currency = self.cleaned_data.get('currency')
        amount = self.cleaned_data.get('amount')
        account = self.cleaned_data.get('account')
        if currency == 'AR$':
            peso = Decimal(account.pesoArBalance)
            peso += amount
            account.pesoArBalance = peso
            
        if currency == 'US$':
            dollar = Decimal(account.dollarBalance)
            dollar += amount
            account.dollarBalance = dollar
            
        if currency == 'EU$':
            euro = Decimal(account.euBalance)
            euro += amount
            account.euBalance = euro
            
        log = ActionsLog(user=self.user, account=account, actionType='Deposito',
            amount=Decimal(self.cleaned_data.get('amount')), currency=self.cleaned_data.get('currency'))
        log.save()
        account.save()

class ExtractionForm(forms.Form):    
    account = forms.ModelChoiceField(
        label='Numero de cuenta', queryset=Account.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}))

    currency = forms.ChoiceField(
        label='Moneda',choices=(('AR$','AR$'),('US$','US$'),('EU$','EU$')),
        widget=forms.Select(attrs={'class':'form-control'}))
    amount = forms.DecimalField(label='Monto',widget=forms.NumberInput(attrs={'class':'form-control','min':'1'}))


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ExtractionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(users__email=self.user.email)
    
    def clean_amount(self):
        currency = self.cleaned_data.get('currency')
        amount = self.cleaned_data.get('amount')
        account = self.cleaned_data.get('account')
        if currency == 'AR$' and amount > Decimal(account.pesoArBalance):
            raise forms.ValidationError('La cuenta seleccionada no tiene fondos(AR$) suficientes.')
            
        elif currency == 'US$' and amount > Decimal(account.dollarBalance):
            raise forms.ValidationError('La cuenta seleccionada no tiene fondos(US$) suficientes.')
            
        elif currency == 'EU$' and amount > Decimal(account.euBalance):
            raise forms.ValidationError('La cuenta seleccionada no tiene fondos(EU$) suficientes.')

        return self.cleaned_data.get('amount')
    
    def save(self, commit=False):
        currency = self.cleaned_data.get('currency')
        amount = self.cleaned_data.get('amount')
        account = self.cleaned_data.get('account')
        if currency == 'AR$':
            peso = Decimal(account.pesoArBalance)
            peso -= amount
            account.pesoArBalance = peso
            
        elif currency == 'US$':
            dollar = Decimal(account.dollarBalance)
            dollar -= amount
            account.dollarBalance = dollar
            
        elif currency == 'EU$':
            euro = Decimal(account.euBalance)
            euro -= amount
            account.euBalance = euro

        log = ActionsLog(user=self.user, account=account, actionType='Extraccion',
            amount=(Decimal(self.cleaned_data.get('amount'))*-1), currency=self.cleaned_data.get('currency'))
        log.save()
        account.save()
        





    
    
        
        
