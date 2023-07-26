from django.contrib import admin
from django.utils.html import format_html
from .models import User, Route, City, Street, Avtomat
from .forms import AvtomatAdminForm, UserAdminForm


class BaseAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(User)
class UserAdmin(BaseAdmin):
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
class RouteAdmin(BaseAdmin):
    list_display = ('name', 'car_number', 'driver_1', 'driver_2')


@admin.register(City)
class CityAdmin(BaseAdmin):
    pass


@admin.register(Street)
class StreetAdmin(BaseAdmin):
    list_display = ('street', 'city')
    search_fields = ('street', )


@admin.register(Avtomat)
class AvtomatAdmin(BaseAdmin):
    form = AvtomatAdminForm
    list_display = ('number', 'address', 'route', 'state', 'show_on_map', 'create_qr')
    search_fields = ('street__street', 'avtomat_number', 'rro_id')
    autocomplete_fields = ('street', )
    list_filter = ('state', 'size', 'price_for_app', 'street__city')
    save_as = True  # Create new Avtomat from existing

    @admin.display(description='')
    def price_type(self, obj=None):
        return obj.street__city

    @admin.display(description='Number', ordering='avtomat_number')
    def number(self, obj):
        return obj.avtomat_number

    @admin.display(ordering='street')
    def address(self, obj=None):
        return 'No Address' if obj.street is None else f'{obj.street} {obj.house}'

    @admin.display(description='')
    def show_on_map(self, obj=None):
        href = f'https://www.google.com/maps/search/?api=1&query={obj.latitude},{obj.longitude}'
        return '' if obj.latitude is None else format_html(f"<a target='_blank' rel='noopener noreferrer'"
                                                           f"href={href}><i class='fas fa-map-marked-alt'></i></a>")

    @admin.display(description='')
    def create_qr(self, obj=None):
        href = f'http://chart.apis.google.com/chart?' \
               f'cht=qr&chs=300x300&' \
               f'chl=https://app.roganska.com?vodomat_id={obj.avtomat_number}'
        return format_html(f"<a target='_blank' rel='noopener noreferrer'"
                           f"href={href}><i class='fas fa-qrcode'></i></a>")

    fieldsets = (
        ('Set Avtomat Number', {
           'fields': ('avtomat_number', )
        }),
        ('Properties', {
            'fields': ('route', 'size', 'competitors', 'price', 'state', 'rro_id',
                       ('security_id', 'security_state'))
        }),
        ('Address', {
            'fields': ('street', 'house', 'latitude', 'longitude')
        }),
        ('Application', {
            'fields': ('price_for_app', 'search_radius', 'payment_app_url', 'payment_gateway_name')
        })
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            return fieldsets[1:]
        return fieldsets


admin.site.site_header = 'Vodomat Admin'
admin.site.site_title = 'Vodomat Admin'
admin.site.site_url = None
