from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegistrationView, ActivationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    
    path('register/', RegistrationView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<str:activation_code>', ActivationView.as_view()),

]