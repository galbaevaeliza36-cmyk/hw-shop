from django.urls import path
from .views import (
    CategoryListView,
    CategoryDetailView,
    ProductListView,
    ProductDetailView,
    ReviewListView,
    ReviewDetailView,
    ProductsReviewsView,
    ConfirmUserView,
)

urlpatterns = [
    path('api/v1/categories/', CategoryListView.as_view()),
    path('api/v1/categories/<int:id>/', CategoryDetailView.as_view()),

    path('api/v1/products/', ProductListView.as_view()),
    path('api/v1/products/<int:id>/', ProductDetailView.as_view()),

    path('api/v1/reviews/', ReviewListView.as_view()),
    path('api/v1/reviews/<int:id>/', ReviewDetailView.as_view()),

    path('api/v1/products/reviews/', ProductsReviewsView.as_view()),

    path('api/v1/users/confirm/', ConfirmUserView.as_view()),
]