from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings

from drf_endpoint_examples.drf import ObjectIsAdminUser, AllVerbDjangoModelPermissions
from drf_endpoint_examples.openapi import ChoicesAutoSchema
from endpoints.models import Customer, Product, Order, Address, Review
from endpoints.serializers import (
    CustomerSerializer,
    ProductSerializer,
    OrderSerializer,
    AddressSerializer,
    ReviewSerializer,
)

PERMISSION_CLASSES = [ObjectIsAdminUser | AllVerbDjangoModelPermissions]
AUTHENTICATION_CLASSES = [
    *api_settings.DEFAULT_AUTHENTICATION_CLASSES,
    TokenAuthentication,
]


class CustomerViewSet(viewsets.ModelViewSet):
    authentication_classes = AUTHENTICATION_CLASSES
    permission_classes = PERMISSION_CLASSES
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    schema = ChoicesAutoSchema()


class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = AUTHENTICATION_CLASSES
    permission_classes = PERMISSION_CLASSES
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    schema = ChoicesAutoSchema()


class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = AUTHENTICATION_CLASSES
    permission_classes = PERMISSION_CLASSES
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    schema = ChoicesAutoSchema()


class AddressViewSet(viewsets.ModelViewSet):
    authentication_classes = AUTHENTICATION_CLASSES
    permission_classes = PERMISSION_CLASSES
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    schema = ChoicesAutoSchema()


class ReviewViewSet(viewsets.ModelViewSet):
    authentication_classes = AUTHENTICATION_CLASSES
    permission_classes = PERMISSION_CLASSES
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    schema = ChoicesAutoSchema()
