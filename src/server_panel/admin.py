from django.contrib import admin
from django.utils.html import format_html
from .models import User, Route, City, Street, Avtomat, Setting
from .forms import AvtomatAdminForm, UserAdminForm
from .avtomat_actions import set_max_sum, set_price

from django.db.models import Count
from .admin_filters import InactiveAvtomatsListFilter


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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

    @admin.display()
    def full_name(self, obj):
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

    list_select_related = ['city', ]


@admin.register(Avtomat)
class AvtomatAdmin(admin.ModelAdmin):
    actions = [set_price, set_max_sum, admin.actions.delete_selected]
    form = AvtomatAdminForm
    list_display = ('number', 'address', 'route', 'state', 'show_on_map', 'create_qr')
    search_fields = ('street__street', 'avtomat_number', 'rro_id')
    autocomplete_fields = ('street', )
    list_filter = ('state', 'size', 'price_for_app', 'route__name', 'street__city')
    save_as = True  # Create new Avtomat from existing
    list_per_page = 100

    list_select_related = ['street', 'street__city', 'route']

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.annotate(statistic_count=Count('statistic'))

    @admin.display(description='')
    def price_type(self, obj):
        return obj.street__city

    @admin.display(description='Number', ordering='avtomat_number')
    def number(self, obj):
        return obj.avtomat_number

    @admin.display(ordering='street')
    def address(self, obj):
        return 'No Address' if obj.street is None else f'{obj.street} {obj.house}'

    @admin.display(description='')
    def show_on_map(self, obj):
        href = f'https://www.google.com/maps/search/?api=1&query={obj.latitude},{obj.longitude}'
        return '' if obj.latitude is None else format_html(f"<a target='_blank' rel='noopener noreferrer'"
                                                           f"href={href}><i class='fas fa-map-marked-alt'></i></a>")

    @admin.display(description='')
    def create_qr(self, obj):
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


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    pass


admin.site.site_header = 'Vodomat Admin'
admin.site.site_title = 'Vodomat Admin'
admin.site.site_url = ''
admin.site.disable_action('delete_selected')
