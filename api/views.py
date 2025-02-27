from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductsInfoSerializer, OrderCreateSerializer, UserSerializer
from api.models import Product, Order, OrderItem, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, AllowAny)
from rest_framework.views import APIView
from rest_framework import viewsets
from api.filters import ProductFilter, InStockFilterBackend, OrderFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ProductListCreateAPIView(generics.ListCreateAPIView):
  #queryset = Product.objects.all()
  queryset = Product.objects.order_by('pk')
  serializer_class = ProductSerializer
  #filterset_fields = ('name', 'price')
  filterset_class = ProductFilter
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, InStockFilterBackend]
  search_fields = ['=name', 'description']
  ordering_fields = ['name', 'price', 'stock']
  #pagination_class = LimitOffsetPagination
  pagination_class = None
  #pagination_class = PageNumberPagination
  """ pagination_class.page_size = 2
  pagination_class.page_query_param = 'pagenum'
  pagination_class.page_size_query_param = 'size'
  pagination_class.max_page_size = 4 """
  
  @method_decorator(cache_page(60*15, key_prefix='products_list'))
  def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)
  
  def get_queryset(self):
    import time
    time.sleep(2)
    return super().get_queryset()
  
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
  
class OrderViewSet(viewsets.ModelViewSet):
  queryset = Order.objects.prefetch_related('items__product')
  serializer_class = OrderSerializer
  #permission_classes = [AllowAny]
  permission_classes = [IsAuthenticated]
  pagination_class = None
  filterset_class = OrderFilter
  filter_backends = [DjangoFilterBackend]
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)
  
  def get_serializer_class(self):
    if self.action == 'create' or self.action == 'update':
      return OrderCreateSerializer
    return super().get_serializer_class()
  
  def get_queryset(self):
    qs = super().get_queryset()
    if not self.request.user.is_staff:
      qs = qs.filter(user=self.request.user)
    return qs
  
  """ @action(
    detail=False, 
    methods=['get'], 
    url_path='user-orders', 
    #permission_classes=[IsAuthenticated]
    )
  def user_orders(self, request):
    orders = self.get_queryset().filter(user=request.user)
    serializer = self.get_serializer(orders, many=True)
    return Response(serializer.data) """
  
""" class OrderListAPIView(generics.ListAPIView):
  queryset = Order.objects.prefetch_related('items__product')
  serializer_class = OrderSerializer """

""" @api_view(['GET'])
def order_list(request):
  orders = Order.objects.prefetch_related('items__product')
  serializer = OrderSerializer(orders, many=True)
  return Response(serializer.data) """
  
""" class UserOrderListAPIView(generics.ListAPIView):
  queryset = Order.objects.prefetch_related('items__product')
  serializer_class = OrderSerializer
  permission_classes = [IsAuthenticated]
  
  def get_queryset(self):
    qs = super().get_queryset()
    return qs.filter(user=self.request.user) """

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
  
class UserListView(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  pagination_class = None