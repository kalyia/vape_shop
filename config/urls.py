from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


from apps.account.views import *
from apps.order.views import OrderViewSet
from apps.cart.views import ShoppingCartViewSet, CartItemViewSet

router = DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register('user_cart', ShoppingCartViewSet, basename='shopping_cart')
router.register('cart_item', CartItemViewSet, basename='cart_item')

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes = [permissions.AllowAny],
)


urlpatterns = [
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('account/', include('apps.account.urls')),
    path('product/', include('apps.product.urls')),
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)