from django.contrib import admin
from django.urls import path, include
from bankAccounts.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('home/', include('bankAccounts.urls')),
    path('login/', include('login.urls')),
]
