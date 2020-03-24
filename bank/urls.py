from django.contrib import admin
from django.urls import path, include
from bankAccounts.views import home
from django.conf.urls import handler404, handler500
from bankAccounts.views import handler404 as handler_404
from bankAccounts.views import handler500 as handler_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('home/', include('bankAccounts.urls')),
    path('login/', include('login.urls')),
]

handler404 = handler_404
handler500 = handler_500