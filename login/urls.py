from django.urls import path
from login.views import login, signIn, signUp, logout

urlpatterns = [
    path('', login),
    path('signIn/', signIn),
    path('signUp/', signUp),
    path('logout/',logout),
]