from django.urls import path
from .views import OrderViewSet

urlpatterns = [
    path('order/', OrderViewSet.as_view({'get': 'order'})),
]