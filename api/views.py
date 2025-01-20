from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductsInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, AllowAny)
from rest_framework.views import APIView

class ProductListCreateAPIView(generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  
  def get_permissions(self):
    self.permission_classes = [AllowAny]
    if self.request.method == 'POST':
      self.permission_classes = [IsAdminUser]
    return super().get_permissions()

""" class ProductListAPIView(generics.ListAPIView): # Class with only get list method
  queryset = Product.objects.all() #get all products
  #queryset = Product.objects.filter(stock__gt=0) #get all products with stock greater than 0
  #queryset = Product.objects.exclude(stock__gt=0) #get all products with stock equal to 0
  serializer_class = ProductSerializer """

""" class ProductCreateAPIView(generics.CreateAPIView): # Class with only the create method
  model = Product
  serializer_class = ProductSerializer
  
  def create(self, request, *args, **kwargs):
    print(request.data)
    return super().create(request, *args, **kwargs)
 """
""" @api_view(['GET']) # As a function-based view
def product_list(request):
  products = Product.objects.all()
  serializer = ProductSerializer(products, many=True)s
  return Response(serializer.data) """

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  #by default, the lookup field is 'pk'
  lookup_url_kwarg = 'product_id'
  
  def get_permissions(self):
    self.permission_classes = [AllowAny]
    if self.request.method in ['PUT', 'PATCH', 'DELETE']:
      self.permission_classes = [IsAdminUser]
    return super().get_permissions()

""" @api_view(['GET'])
def product_detail(request, pk):
  product = get_object_or_404(Product, pk=pk)
  serializer = ProductSerializer(product)
  return Response(serializer.data) """
  
class OrderListAPIView(generics.ListAPIView):
  queryset = Order.objects.prefetch_related('items__product')
  serializer_class = OrderSerializer

""" @api_view(['GET'])
def order_list(request):
  orders = Order.objects.prefetch_related('items__product')
  serializer = OrderSerializer(orders, many=True)
  return Response(serializer.data) """
  
class UserOrderListAPIView(generics.ListAPIView):
  queryset = Order.objects.prefetch_related('items__product')
  serializer_class = OrderSerializer
  permission_classes = [IsAuthenticated]
  
  def get_queryset(self):
    qs = super().get_queryset()
    return qs.filter(user=self.request.user)

""" @api_view(['GET'])
def product_info(request):
  products = Product.objects.all()
  serializer = ProductsInfoSerializer({
    'products': products,
    'count': len(products),
    'max_price': products.aggregate(max_price=Max('price'))['max_price']
  })
  return Response(serializer.data) """
  
class ProductInfoAPIView(APIView):
  def get(self, request):
    products = Product.objects.all()
    serializer = ProductsInfoSerializer({
      'products': products,
      'count': len(products),
      'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)