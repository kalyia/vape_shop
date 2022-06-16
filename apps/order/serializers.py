from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        total_sum = 0
        request = self.context.get('request')
        user = request.user
        order = Order.objects.create(**validated_data)
        order.save()
        return order

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['shopping_cart'] = instance.shopping_cart.user.username
        return rep