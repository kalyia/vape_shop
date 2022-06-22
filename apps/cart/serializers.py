from rest_framework import serializers

from .models import CartItem, ShoppingCart


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity')

    def validate(self, attrs):
        cart_shopping = self.context.get("request").user.cart
        attrs['cart'] = cart_shopping
        return attrs

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep['product'] = instance.product.title
            rep['total_price'] = instance.get_total_price_item()
            rep['cart'] = instance.cart_shopping.id
            return rep
        except:
            return rep


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep['user'] = instance.user.email
            rep['products'] = CartItemSerializer(instance.cart_items, many=True).data
            rep['total_price'] = instance.get_total_price_sum()
            return rep
        except:
            return rep