from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение пользователя в административной панели."""
    list_display = ('id', 'email', 'is_active', 'groups_display')
    filter_horizontal = ('groups', 'user_permissions',)

    def groups_display(self, obj):
        groups = obj.groups.all()
        if groups:
            return ', '.join([group.name for group in groups])
        else:
            return 'Не состоит в группах'

    groups_display.short_description = 'Группы'
