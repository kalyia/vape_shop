from rest_framework import serializers
from .models import Product, ProductImage, Review, LikeProduct, SimilarProduct


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Product
        exclude = ('create_date', 'update_date')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = instance.category.name
        representation['author'] = instance.author.email
        representation['images'] = ProductImageSerializer(instance.images.all(),
                                                  many=True, context=self.context).data
        representation['reviews'] = ReviewProductSerializer(instance.reviews.all(),
                                                  many=True, context=self.context).data

        representation['likes'] = instance.likes.filter(is_like=True).count()
        return representation


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')

            if request is not None:
                url = request.build_absolute_uri(url)

        else:
            url = ''

        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        representation['product'] = instance.product.title
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


class SimilarProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = SimilarProduct
        fields = ['category', 'price']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = instance.product.title
        return representation


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    products = SimilarProductSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' 