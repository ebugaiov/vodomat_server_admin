from django.contrib import admin
from .models import User, City


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'permission', 'last_visit')

    @admin.display
    def full_name(self, obj=None):
        return f'{obj.last_name} {obj.first_name}' if obj.last_name else ''


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


admin.site.site_header = 'Vodomat Server Admin'
