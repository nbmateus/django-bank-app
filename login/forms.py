from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate


class SignUpForm(forms.ModelForm):
    email = forms.CharField(max_length=30, label='Email', widget=forms.TextInput(attrs={'class':"form-control",'pattern':'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2, 4}$+'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control','pattern':'[a-zA-Z0-9]+'}))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class':'form-control','pattern':'[a-zA-Z0-9]+'}))


    class Meta:
        model = User
        fields = ('email',)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas deben ser iguales.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class':"form-control"}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        user = authenticate(email= self.cleaned_data.get('email'), password = self.cleaned_data.get('password'))
        if  user is None:
            raise forms.ValidationError("Email o contraseña incorrecta.")
        return self.cleaned_data



class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_admin')

    def clean_password(self):
        return self.initial["password"]