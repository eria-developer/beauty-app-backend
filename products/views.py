from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Product, Category, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer
from django.db.models import F
from django.db import transaction
from accounts.models import User

class ProductView(GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    # Create a new Product
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=request.user)  # Assign the logged-in user as the seller
        return Response({'message': 'Product created successfully'}, status=status.HTTP_201_CREATED)

    # Retrieve or list all products
    def get(self, request, pk=None):
        if pk:
            product = get_object_or_404(Product, pk=pk)
            serializer = self.serializer_class(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            products = Product.objects.all()
            serializer = self.serializer_class(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a product by ID
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk, seller=request.user)  # Ensure that only the seller can update
        serializer = self.serializer_class(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)

    # Delete a product by ID
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk, seller=request.user)  # Ensure that only the seller can delete
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ProductSearchView(ListAPIView):
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]  # Only authenticated users can search for products

    def get_queryset(self):
        name = self.request.query_params.get('name', '')
        category = self.request.query_params.get('category', '')
        
        queryset = Product.objects.all()
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category=category)

        return queryset
    



class CategoryView(GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # Retrieve or list all categorys
    def get(self, request, pk=None):
        if pk:
            category = get_object_or_404(Category, pk=pk)
            serializer = self.serializer_class(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            categorys = Category.objects.all()
            serializer = self.serializer_class(categorys, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



class CategorySearchView(ListAPIView):
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticated]  # Only authenticated users can search for categorys

    def get_queryset(self):
        name = self.request.query_params.get('name', '')
        
        queryset = Category.objects.all()
        
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset
    




class CheckoutView(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart_items = request.data.get('items', [])
        if not cart_items:
            return Response({'error': 'No items in cart'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user)
        
        for item in cart_items:
            product_id = item.get('productId')
            quantity = item.get('quantity')
            product = get_object_or_404(Product, id=product_id)

            if product.stock:
                if product.stock < quantity:
                    order.delete()
                    return Response({'error': f'Not enough stock for {product.name}'}, status=status.HTTP_400_BAD_REQUEST)
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            # Update product stock
            if product.stock:
                product.stock -= quantity
            product.save()
        
        # Calculate and add loyalty points
        loyalty_points = order.calculate_loyalty_points()
        order.loyalty_points_earned = loyalty_points
        order.save()

        # Update user's total loyalty points
        user = User.objects.select_for_update().get(id=request.user.id)
        user.loyalty_points = (user.loyalty_points or 0) + loyalty_points
        user.save()
        
        order_serializer = self.serializer_class(order)
        return Response({
            'order': order_serializer.data,
            'loyalty_points_earned': loyalty_points,
            'total_loyalty_points': user.loyalty_points
        }, status=status.HTTP_201_CREATED)



class UserOrdersView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')