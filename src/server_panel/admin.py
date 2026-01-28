import csv
import io

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Q
from .models import User, Route, City, Street, Avtomat, Setting
from .forms import AvtomatAdminForm, UserAdminForm
from .avtomat_actions import set_max_sum, set_price, set_price_for_app, disable_online_pay

from .admin_filters import RoutesListFilter


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
    actions = [set_price, set_price_for_app, set_max_sum, disable_online_pay, admin.actions.delete_selected]
    form = AvtomatAdminForm
    list_display = ('number', 'address', 'route', 'state', 'show_on_map', 'create_qr')
    search_fields = ('street__street', 'avtomat_number', 'rro_id')
    autocomplete_fields = ('street', )
    list_filter = ('state', 'size', 'price_for_app', RoutesListFilter, 'street__city')
    save_as = True  # Create new Avtomat from existing
    list_per_page = 100

    list_select_related = ['street', 'street__city', 'route']

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
            'fields': ('visible_in_app', 'price_for_app', 'search_radius', 'payment_app_url', 'payment_gateway_name')
        })
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            return fieldsets[1:]
        return fieldsets

    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST' and 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']

            # Read CSV and extract machine identifiers
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string)

            # Skip header if present
            # next(reader, None)

            # Extract identifiers (adjust based on your CSV format)
            machine_ids = [row[0] for row in reader if row]

            # Store in session for filtering
            request.session['machine_filter_ids'] = machine_ids

        # Clear filter if requested
        if request.GET.get('clear_csv_filter'):
            request.session.pop('machine_filter_ids', None)

        return super().changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Apply CSV filter if exists
        machine_ids = request.session.get('machine_filter_ids')
        if machine_ids:
            # Filter by ID, name, or serial number - adjust as needed
            qs = qs.filter(
                Q(avtomat_number__in=machine_ids)
            )

        return qs


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    pass


admin.site.site_header = 'Vodomat Admin'
admin.site.site_title = 'Vodomat Admin'
admin.site.site_url = ''
admin.site.disable_action('delete_selected')
