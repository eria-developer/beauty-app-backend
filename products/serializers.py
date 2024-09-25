from rest_framework import serializers
from .models import Product, Category, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' 


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' 



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()
    total_amount = serializers.SerializerMethodField()
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES, required=False)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'is_paid', 'status', 'items', 'loyalty_points_earned', 'total_amount']

    def get_total_amount(self, obj):
        return sum(item.get_total_price() for item in obj.items.all())