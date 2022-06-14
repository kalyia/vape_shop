from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.cart.views import ShoppingCartViewSet, CartItemViewSet

router = SimpleRouter()
router.register('user_cart', ShoppingCartViewSet, basename='shopping_cart')
router.register('cart_item', CartItemViewSet, basename='cart_item')

urlpattenrs = [
    path('', include(router.urls)),
]