from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from trading_network.filters import LinkFilter
from trading_network.models import Contact, Product, Link
from trading_network.serializers import ContactSerializer, ProductSerializer, LinkSerializer, LinkReadSerializer


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LinkCreateAPIView(generics.CreateAPIView):
    serializer_class = LinkSerializer


class LinkUpdateAPIView(generics.UpdateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class LinkListAPIView(generics.ListAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkReadSerializer
    filterset_class = LinkFilter


class LinkRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkReadSerializer


class LinkDestroyAPIView(generics.DestroyAPIView):
    queryset = Link.objects.all()
    permission_classes = [IsAdminUser]
