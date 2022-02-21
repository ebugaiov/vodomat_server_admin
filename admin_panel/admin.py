from django.contrib import admin
from .models import User, Route, City, Street, Avtomat
from .forms import UserAdminForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'permission', 'last_visit')

    form = UserAdminForm
    fieldsets = (
        (None, {
            'fields': ('username', 'last_name', 'first_name', 'email', 'permission')
        }),
        ('Password', {
            'fields': ('password', 'confirm_password')
        })
    )

    @admin.display
    def full_name(self, obj=None):
        return f'{obj.last_name} {obj.first_name}' if obj.last_name else ''


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_number', 'driver_1', 'driver_2')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('street', 'city')
    search_fields = ('street', )


@admin.register(Avtomat)
class AvtomatAdmin(admin.ModelAdmin):
    list_display = ('avtomat_number', 'address', 'route', 'price_for_app', 'size', 'competitors')
    search_fields = ('street__street', 'house')
    autocomplete_fields = ('street', )
    list_filter = ('size', 'competitors', 'price_for_app', 'route')

    @admin.display
    def address(self, obj=None):
        return 'No Address' if obj.street is None else f'{obj.street} {obj.house}'

    fieldsets = (
        (None, {
            'fields': ('route', 'size', 'competitors', 'price')
        }),
        ('Address', {
            'fields': ('street', 'house', 'latitude', 'longitude')
        }),
        ('Application', {
            'fields': ('price_for_app', 'search_radius', 'payment_app_url', 'payment_gateway_url')
        })
    )


admin.site.site_header = 'Vodomat Server Admin'
