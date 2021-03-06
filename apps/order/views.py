import django_filters.rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializer
from .filters import OrderFilter
from .permissions import DenyAll


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = OrderFilter
    ordering_fields = ['total_sum', 'created_at']


    def get_permissions(self):
        if self.action in ['create', 'list',
                           'retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        else:
            return [DenyAll()]
