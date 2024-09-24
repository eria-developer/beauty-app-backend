from django.urls import path
from .views import ProductView, ProductSearchView, CategorySearchView, CategoryView, CheckoutView, UserOrdersView, AdminOrdersView

urlpatterns = [
    # Product URLs
    path('products/', ProductView.as_view(), name='product_list_create'),  # List and Create Products
    path('products/<int:pk>/', ProductView.as_view(), name='product_detail'),  # Retrieve, Update, Delete Product
    path('products/search/', ProductSearchView.as_view(), name='product_search'),  # Search Products

    # Category URLs
    path('categories/', CategoryView.as_view(), name='category_list_create'),
    path('categories/search/', CategorySearchView.as_view(), name='category_search'),

    # Checkout and Orders
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('user-orders/', UserOrdersView.as_view(), name='user_orders'),

    # Seller Orders
    # path('seller-orders/', SellerOrdersView.as_view(), name='seller_orders'),  # List all seller orders
    # path('seller-orders/<int:pk>/update-status/', SellerOrdersView.as_view(), name='update_order_status'),  # Update order status
    
    # product urls 
    path('products/', ProductView.as_view(), name='product_list_create'),  # List and Create Products
    path('products/<int:pk>/', ProductView.as_view(), name='product_detail'),  # Retrieve, Update, Delete Product
    path('products/search/', ProductSearchView.as_view(), name='product_search'),  # Search Products

    # categories urls 
    path('categories/', CategoryView.as_view(), name='category_list_create'),
    path('categories/search/', CategorySearchView.as_view(), name='category_search'),

    # checking out views
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('user-orders/', UserOrdersView.as_view(), name='user_orders'),

    # User Orders
    path('user-orders/', UserOrdersView.as_view(), name='user_orders'),
    path('user-orders/<int:pk>/', UserOrdersView.as_view(), name='user_order_detail'),

    # Admin Orders
    path('admin-orders/', AdminOrdersView.as_view(), name='admin_orders'),
    path('admin-orders/<int:pk>/', AdminOrdersView.as_view(), name='admin_order_detail'),
    path('admin-orders/<int:pk>/update-status/', AdminOrdersView.as_view(), name='update_order_status'),
]
