from django.contrib import admin
from django.urls import path, include
from apps.account.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('apps.account.urls')),
]