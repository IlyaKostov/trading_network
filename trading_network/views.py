from django.shortcuts import render
from django_filters import OrderingFilter
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from trading_network.models import Contact, Product, Link
from trading_network.serializers import ContactSerializer, ProductSerializer, LinkSerializer


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LinkCreateAPIView(generics.CreateAPIView):
    serializer_class = LinkSerializer


class LinkListAPIView(generics.ListAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    filterset_fields = ['contact__country']

