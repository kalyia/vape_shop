from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register('reviews', ReviewProductView)
router.register('', ProductViewSet)
router.register('', LikeProductView)

urlpatterns = [
    path('', include(router.urls)),
]