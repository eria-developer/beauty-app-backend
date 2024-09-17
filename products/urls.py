from django.urls import path
from .views import ProductView, ProductSearchView, CategorySearchView, CategoryView, CheckoutView

urlpatterns = [
    # product urls 
    path('products/', ProductView.as_view(), name='product_list_create'),  # List and Create Products
    path('products/<int:pk>/', ProductView.as_view(), name='product_detail'),  # Retrieve, Update, Delete Product
    path('products/search/', ProductSearchView.as_view(), name='product_search'),  # Search Products

    # categories urls 
    path('categories/', CategoryView.as_view(), name='category_list_create'),
    path('categories/search/', CategorySearchView.as_view(), name='category_search'),

    # checking out views
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
