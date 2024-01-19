from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ngettext

from trading_network.forms import LinkAdminForm
from trading_network.models import Link, Product, Contact


@admin.action(description='Очистить задолженность перед поставщиками у выбранных объектов')
def clean_debt(modeladmin, request, queryset):
    updated = queryset.update(debt=None)
    print(updated)
    modeladmin.message_user(
        request,
        ngettext(
            "%d задолженность успешно очищена",
            "%d задолженности успешно очищены",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


class ContactInline(admin.StackedInline):
    model = Contact
    extra = 0
    min_num = 1
    can_delete = False


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'supplier_link', 'level', 'debt', 'created_at')
    list_filter = ('contact__city',)
    list_display_links = ('id', 'name')
    filter_horizontal = ('products', )
    readonly_fields = ('level', 'created_at')
    inlines = [ContactInline]
    actions = [clean_debt]
    form = LinkAdminForm

    def supplier_link(self, obj):
        # Возвращает ссылку на поставщика
        if obj.supplier:
            link = reverse('admin:trading_network_link_change', args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', link, obj.supplier)
        else:
            return None

    supplier_link.short_description = 'ссылка на «Поставщика»'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'model', 'date', 'supplier_list')
    list_display_links = ('id', 'name')
    readonly_fields = ('supplier_list',)

    def supplier_list(self, obj):
        return ', '.join([link.name for link in obj.link_set.all()])

    supplier_list.short_description = 'Список поставщиков использующих продукт'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'link')
    readonly_fields = ('link',)
