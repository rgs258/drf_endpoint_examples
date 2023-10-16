from rest_framework import viewsets

from drf_endpoint_examples.openapi import ChoicesAutoSchema
from endpoints.models import Customer, Product, Order, Address, Review
from endpoints.serializers import (
    CustomerSerializer,
    ProductSerializer,
    OrderSerializer,
    AddressSerializer,
    ReviewSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    schema = ChoicesAutoSchema()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    schema = ChoicesAutoSchema()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    schema = ChoicesAutoSchema()


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    schema = ChoicesAutoSchema()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    schema = ChoicesAutoSchema()
