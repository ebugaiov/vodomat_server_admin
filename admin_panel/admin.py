from django.contrib import admin
from .models import User, Route, City, Street, Avtomat
from .forms import UserAdminForm


class SetupDatabase(admin.ModelAdmin):
    using = 'vodomat_server'

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


@admin.register(User)
class UserAdmin(SetupDatabase):
    list_display = ('username', 'full_name', 'email',
                    'permission', 'last_visit')

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
class RouteAdmin(SetupDatabase):
    list_display = ('name', 'car_number', 'driver_1', 'driver_2')


@admin.register(City)
class CityAdmin(SetupDatabase):
    pass


@admin.register(Street)
class StreetAdmin(SetupDatabase):
    list_display = ('street', 'city')
    search_fields = ('street', )


@admin.register(Avtomat)
class AvtomatAdmin(SetupDatabase):
    list_display = ('number', 'address', 'route', 'state')
    search_fields = ('street__street', 'avtomat_number')
    autocomplete_fields = ('street', )
    list_filter = ('state', 'size', 'price_for_app')

    def number(self, obj):
        return obj.avtomat_number

    number.short_description = 'Number'
    number.admin_order_field = 'avtomat_number'

    def address(self, obj=None):
        return 'No Address' if obj.street is None else f'{obj.street} {obj.house}'

    address.admin_order_field = 'street'

    fieldsets = (
        (None, {
            'fields': ('route', 'size', 'competitors', 'price', 'state')
        }),
        ('Address', {
            'fields': ('street', 'house', 'latitude', 'longitude')
        }),
        ('Application', {
            'fields': ('price_for_app', 'search_radius', 'payment_app_url', 'payment_gateway_url')
        })
    )


admin.site.site_header = 'Vodomat Server Admin'
admin.site.site_url = None
