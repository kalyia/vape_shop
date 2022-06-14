from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register('images', ProductImageView)
router.register('reviews', ReviewProductView)
router.register('', ProductViewSet)

urlpatterns = [
    path('product/', include(router.urls)),
]