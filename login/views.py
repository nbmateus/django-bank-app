from django.shortcuts import render, redirect
from .models import User
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login as authLogin
from django.contrib.auth import logout as authLogout
from django.http import JsonResponse

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'login/login.html', {'logForm':LoginForm(),'regForm':SignUpForm()})

def signIn(request):
    logForm = LoginForm(request.POST)
    response = {'redirectUrl':'/'}
    if logForm.is_valid():
        user = User.objects.get(email=logForm.cleaned_data.get('email'))
        authLogin(request, user)
        return JsonResponse(response)
    response['errors'] = logForm.errors
    return JsonResponse(response)

def signUp(request):
    regForm = SignUpForm(request.POST)
    response = {"redirectUrl":"/"}
    if regForm.is_valid():
        user = regForm.save()
        authLogin(request, user)
        return JsonResponse(response)
    response["errors"] = regForm.errors
    return JsonResponse(response)


def logout(request):
    authLogout(request)
    return redirect('/')
