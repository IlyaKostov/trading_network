from rest_framework import serializers

from trading_network.models import Link, Contact, Product
from trading_network.validators import ProductSupplierRelationshipValidator, StatusLinkSupplierValidator


class RepresentationMixin:
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status_link'] = instance.get_status_link_display()
        return representation


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ('link',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class LinkSerializer(RepresentationMixin, serializers.ModelSerializer):
    """Сериализатор привычек"""
    contact = ContactSerializer(required=True, many=True, source='contact_set')

    class Meta:
        model = Link
        fields = ['id', 'status_link', 'supplier', 'name', 'level', 'products', 'debt', 'contact']
        read_only_fields = ['debt', 'level']
        validators = [StatusLinkSupplierValidator('status_link', 'supplier', 'debt'),
                      ProductSupplierRelationshipValidator('supplier', 'products')]

    def create(self, validated_data):
        contacts = validated_data.pop('contact_set')
        products = validated_data.pop('products')
        link = Link.objects.create(**validated_data)
        for contact in contacts:
            Contact.objects.create(link=link, **contact)
        link.products.set(products)
        return link

    def update(self, instance, validated_data):
        instance.status_link = validated_data.get('status_link', instance.status_link)
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.name = validated_data.get('name', instance.name)

        products_data = validated_data.get('products')
        if products_data is not None:
            instance.products.set(products_data)

        instance.save()

        contact_data = validated_data.pop('contact_set')
        contacts = instance.contact_set.all()

        for i, contact in enumerate(contacts):
            contact_info = contact_data[i]
            contact.email = contact_info.get('email', contact.email)
            contact.country = contact_info.get('country', contact.country)
            contact.city = contact_info.get('city', contact.city)
            contact.street = contact_info.get('street', contact.street)
            contact.num_house = contact_info.get('num_house', contact.num_house)
            contact.save()

        return instance


class LinkReadSerializer(RepresentationMixin, serializers.ModelSerializer):
    """Сериализатор привычек"""
    contact = ContactSerializer(many=True, source='contact_set')
    products = ProductSerializer(many=True)
    supplier = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ['id', 'status_link', 'supplier', 'name', 'level', 'products', 'debt', 'contact']

    def get_supplier(self, obj):
        return obj.supplier.__str__()
