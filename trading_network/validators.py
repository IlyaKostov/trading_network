from django.utils.translation import ngettext
from rest_framework import serializers


class StatusLinkSupplierValidator:
    """Валидация установки поставщика и иерархической структуры"""
    def __init__(self, status, supplier):
        self.status = status
        self.supplier = supplier

    def __call__(self, attrs):
        status_link_ = attrs.get(self.status)
        supplier_ = attrs.get(self.supplier)
        if status_link_ == 'factory' and supplier_:
            raise serializers.ValidationError('У завода не может быть Поставщика')
        if supplier_ is None and (status_link_ != 'factory' and status_link_):
            raise serializers.ValidationError('Без поставщика может быть только Завод')
        if supplier_ and supplier_.level == 2:
            raise serializers.ValidationError('Иерархическая структура не может состоять более чем из 3 уровней')


class ProductSupplierRelationshipValidator:
    """Валидация наличия продукта у определенного поставщика"""
    def __init__(self, supplier, products):
        self.supplier = supplier
        self.products = products

    def __call__(self, attrs):
        supplier_ = attrs.get(self.supplier)
        product_list_ = attrs.get(self.products)
        if supplier_ and product_list_:
            supplier_products = supplier_.products.all()
            products = [product.name for product in product_list_ if product not in supplier_products]
            if products:
                raise serializers.ValidationError(
                    ngettext(
                        "Продукт %s не принадлежит поставщику %s",
                        "Продукты %s не принадлежат поставщику %s",
                        len(products),
                    )
                    % (', '.join(products), supplier_.name)
                )
