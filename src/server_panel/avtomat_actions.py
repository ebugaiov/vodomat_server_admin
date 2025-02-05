import os
import requests
from typing import Optional
from django.contrib import admin, messages
from django.core.cache import cache
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str
from .models import Setting

# Utility Functions

def get_api_key() -> Optional[str]:
    """Retrieve the API key from cache or request a new one."""
    api_key = cache.get('api_key')
    if api_key is None:
        credentials = {
            'username': os.getenv('SERVER_API_USER'),
            'password': os.getenv('SERVER_API_PASSWORD')
        }
        response = requests.post(f'{os.getenv("SERVER_API_URL")}/api_key', data=credentials)
        if response.status_code == 200:
            api_key = response.json().get('api_key')
            cache.set('api_key', api_key, timeout=3600)
    return api_key


def set_param_for_avtomat(avtomat_number: int, param: str) -> Optional[int]:
    """Send a parameter setting request for a given avtomat."""
    request_body = {'avtomat_number': avtomat_number, 'param': param}
    headers = {os.getenv('SERVER_API_SECURE_HEADERS'): get_api_key()}
    response = requests.post(f'{os.getenv("SERVER_API_URL")}/param', json=request_body, headers=headers)
    if response.status_code == 200:
        return response.json().get('avtomat_number')
    return None


def log_change(request, obj, message: str):
    """Log an admin action for a given object."""
    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=force_str(obj),
        action_flag=CHANGE,
        change_message=message,
    )


def get_setting_value(setting_name: str) -> Optional[int]:
    """Fetch a setting value by name, handling missing cases."""
    try:
        return int(Setting.objects.get(name=setting_name).value)
    except Setting.DoesNotExist:
        return None

# Admin Actions

@admin.action(description='Set Max Sum')
def set_max_sum(modeladmin, request, queryset):
    command = '055be4'
    max_sum_value = get_setting_value('avtomat_max_sum')

    if max_sum_value is None:
        messages.warning(request, 'You have to set "avtomat_max_sum" in the settings table.')
        return

    max_sum_hex = f"{max_sum_value:04x}"
    parameter = f'{command}00{max_sum_hex[2:]}{max_sum_hex[:2]}'
    busy_avtomats = []

    for item in queryset:
        busy_avtomat_number = set_param_for_avtomat(item.avtomat_number, parameter)
        if busy_avtomat_number:
            busy_avtomats.append(busy_avtomat_number)
        else:
            log_change(request, item, f'Changed Max Sum to {max_sum_value}')

    if busy_avtomats:
        busy_list = ', '.join(str(avtomat) for avtomat in busy_avtomats)
        messages.warning(request, f"Avtomat(s) busy: {busy_list}")
    else:
        messages.info(request, 'The maximum sum for selected avtomats was set.')


@admin.action(description='Set Price')
def set_price(modeladmin, request, queryset):
    price = get_setting_value('avtomat_price')

    if price is None:
        messages.warning(request, 'You have to set "avtomat_price" in the settings table.')
        return

    for item in queryset:
        item.price = price
        item.save()
        log_change(request, item, f'Changed Price to {price / 100:.2f}')

    messages.info(request, f"Avtomat's Price changed to {price / 100:.2f}")


@admin.action(description='Set Price for App')
def set_price_for_app(modeladmin, request, queryset):
    price_for_app = get_setting_value('avtomat_price_for_app')

    if price_for_app is None:
        messages.warning(request, 'You have to set "avtomat_price_for_app" in the settings table.')
        return

    for item in queryset:
        item.price_for_app = price_for_app
        item.save()
        log_change(request, item, f'Changed Price for App to {price_for_app / 100:.2f}')

    messages.info(request, f"Avtomat's Price for App changed to {price_for_app / 100:.2f}")


@admin.action(description='Disable Online Pay')
def disable_online_pay(modeladmin, request, queryset):
    for item in queryset:
        item.price_for_app = None
        item.save()
        log_change(request, item, 'Changed Price for App (set to None)')

    messages.info(request, "Online Payments have been disabled for the selected avtomats.")
