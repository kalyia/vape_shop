from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register('reviews', ReviewProductView)
router.register('', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('like/', LikeProductView.as_view()),
]