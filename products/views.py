from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer

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
    permission_classes = [IsAuthenticated]  # Only authenticated users can search for products

    def get_queryset(self):
        name = self.request.query_params.get('name', '')
        category = self.request.query_params.get('category', '')
        
        queryset = Product.objects.all()
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category=category)

        return queryset
