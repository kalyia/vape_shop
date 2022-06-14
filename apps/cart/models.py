from django.db import models

from apps.account.models import CustomUser
from apps.product.models import Product

class ShoppingCart(models.Model):

    user = models.OneToOneField(
        to=CustomUser, on_delete=models.CASCADE, related_name='cart'
    )

    def get_total_price_sum(self):
        cart_items = self.cart_items.all()
        total = sum([item.get_total_price_item for item in cart_items])

    def __str__(self):
        return self.user.username


class CartItem(models.Model):

    product = models.ForeignKey(
        to=Product, on_delete=models.SET_NULL, null=True,
        related_name='cart_products'
    )
    cart = models.ForeignKey(
        to=ShoppingCart, on_delete=models.SET_NULL, null=True,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price_item(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.title