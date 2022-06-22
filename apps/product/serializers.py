from rest_framework import serializers
from .models import Product, Review, LikeProduct


class ProductSerializer(serializers.ModelSerializer):
    
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reviews'] = ReviewProductSerializer(instance.reviews.all(),
                                                  many=True, context=self.context).data

        representation['likes'] = instance.likes.filter(is_like=True).count()
        return representation


class ReviewProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        exclude = ('author', )

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['author'] = request.user
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['product'] = instance.product.title
        return representation


class LikeProductSerializer(serializers.ModelSerializer):
    
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LikeProduct
        fields = "__all__"


class FavoriteListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__' 