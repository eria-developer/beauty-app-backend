from django.urls import path
from .views import ProductView, ProductSearchView, CategorySearchView, CategoryView, CheckoutView, UserOrdersView, AdminOrdersView, RedeemLoyaltyPointsView

urlpatterns = [
    # Product URLs
    path('products/', ProductView.as_view(), name='product_list_create'),
    path('products/<int:pk>/', ProductView.as_view(), name='product_detail'),
    path('products/search/', ProductSearchView.as_view(), name='product_search'),
    path('redeem-loyalty-points/', RedeemLoyaltyPointsView.as_view(), name='redeem_loyalty_points'),

    # Category URLs
    path('categories/', CategoryView.as_view(), name='category_list_create'),
    path('categories/search/', CategorySearchView.as_view(), name='category_search'),

    # Checkout
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    # User Orders
    path('user-orders/', UserOrdersView.as_view(), name='user_orders'),
    path('user-orders/<int:pk>/', UserOrdersView.as_view(), name='user_order_detail'),

    # Admin Orders
    path('admin-orders/', AdminOrdersView.as_view(), name='admin_orders'),
    path('admin-orders/<int:pk>/', AdminOrdersView.as_view(), name='admin_order_detail'),
    path('admin-orders/<int:pk>/update-status/', AdminOrdersView.as_view(), name='update_order_status'),
]