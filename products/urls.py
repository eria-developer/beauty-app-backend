from django.urls import path
from .views import ProductView, ProductSearchView

urlpatterns = [
    path('products/', ProductView.as_view(), name='product_list_create'),  # List and Create Products
    path('products/<int:pk>/', ProductView.as_view(), name='product_detail'),  # Retrieve, Update, Delete Product
    path('products/search/', ProductSearchView.as_view(), name='product_search'),  # Search Products
]
