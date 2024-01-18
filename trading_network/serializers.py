from rest_framework import serializers

from trading_network.models import Link, Contact, Product


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    """Сериализатор привычек"""

    class Meta:
        model = Link
        fields = '__all__'
