from django.urls import path

from apps.category.views import *

urlpatterns = [
    path('list/', ListCategoryView.as_view()),
    path('create/', CreateCategoryView.as_view()),
    path('<int:pk>/', RetrieveCategoryView.as_view(),),
    path('update/<int:pk>/', UpdateCategoryView.as_view()),
    path('delete/<int:pk>/', DestroyCategoryView.as_view()),

]