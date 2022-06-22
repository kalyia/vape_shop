from rest_framework.viewsets import ModelViewSet

from .models import ShoppingCart, CartItem
from .serializers import CartItemSerializer, ShoppingCartSerializer


class ShoppingCartViewSet(ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
