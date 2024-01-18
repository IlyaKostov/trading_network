from django import forms
from django.utils.translation import ngettext

from trading_network.models import Link


class LinkAdminForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        status_link = cleaned_data.get('status_link')
        supplier = cleaned_data.get('supplier')
        debt = cleaned_data.get('debt')
        product_list = cleaned_data.get('products')
        if status_link == 'factory' and (supplier or debt):
            raise forms.ValidationError('У завода не может быть Поставщика / Задолженности перед поставщиком')
        if supplier is None and status_link != 'factory':
            raise forms.ValidationError('Без поставщика может быть только Завод')
        if supplier:
            supplier_products = supplier.products.all()
            products = [product.name for product in product_list if product not in supplier_products]
            if products:
                raise forms.ValidationError(
                    ngettext(
                        "Продукт %s не принадлежит поставщику %s",
                        "Продукты %s не принадлежат поставщику %s",
                        len(products),
                    )
                    % (', '.join(products), supplier.name)
                )
        return cleaned_data
