from rest_framework.exceptions import ValidationError


class StatusLinkInLinkValidator:
    """Запрет на ввод поставщика для завода"""

    def __call__(self, attrs):
        print(attrs)
        status_link = attrs.get('status_link')
        supplier = attrs.get('supplier')
        print(status_link)
        if status_link == 'factory' and supplier is not None:
            raise ValidationError('У завода не может быть поставщика')