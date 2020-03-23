from django.contrib import admin
from django.urls import path, include
from bankAccounts.views import home
from django.conf.urls import handler404
from bankAccounts.views import handler404 as handler_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('home/', include('bankAccounts.urls')),
    path('login/', include('login.urls')),
]

handler404 = handler_404