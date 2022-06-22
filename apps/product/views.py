from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import action
import django_filters.rest_framework as filters


from .paginations import ProductPagination
from .models import Product, Review, LikeProduct, Favorite
from .serializers import *


class ProductViewSet(ModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ['category', 'price']
    ordering_fields = ['category', 'title', 'price']
    permission_classes = [IsAuthenticatedOrReadOnly ]
    pagination_class = ProductPagination
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        elif self.action in ['likes', ]:
            return [IsAuthenticated()]
        return []

    # products/id/like/
    @action(detail=True, methods=['GET'])
    def like(self, request, pk):
        product = self.get_object()
        user = request.user
        fav, created = LikeProduct.objects.get_or_create(product=product, user=user)
        if fav.is_like == False:
            fav.is_like = not fav.is_like
            fav.save()
            return Response('You liked this product')
        else:
            fav.is_like = not fav.is_like
            fav.save()
            return Response('You disliked this product')

    # product/id/favorite/
    @action(detail=True, methods=['GET'])
    def favorite(self, request, pk):
        product = self.get_object()
        user = request.user
        fav, created = Favorite.objects.get_or_create(product=product, user=user)
        if fav.favorite == False:
            fav.favorite = not fav.favorite
            fav.save()
            return Response('Added to Favorites')
        else:
            fav.favorite = not fav.favorite
            fav.save()
            return Response('Not in Favorites')


class ReviewProductView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class LikeProductView(ModelViewSet):
    queryset = LikeProduct.objects.all()
    serializer_class = LikeProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class FavoriteView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = FavoriteListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(favorites__user=self.request.user, favorites__favorite=True)
        return queryset

