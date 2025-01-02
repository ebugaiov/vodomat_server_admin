import os
import requests
from typing import Optional
from django.contrib import admin, messages
from django.core.cache import cache
from .models import Setting


def get_api_key() -> str:
    api_key = cache.get('api_key')
    if api_key is None:
        credentials = {'username': os.getenv('SERVER_API_USER'), 'password': os.getenv('SERVER_API_PASSWORD')}
        resp = requests.post(f'{os.getenv("SERVER_API_URL")}/api_key', data=credentials)
        api_key = resp.json().get('api_key')
        cache.set('api_key', api_key, timeout=3600)
    return api_key


def set_param_for_avtomat(avtomat_number: int, param: str) -> Optional[int]:
    request_body = {'avtomat_number': avtomat_number, 'param': param}
    headers = {os.getenv('SERVER_API_SECURE_HEADERS'): get_api_key()}
    resp = requests.post(f'{os.getenv("SERVER_API_URL")}/param', json=request_body, headers=headers)
    return resp.json().get('avtomat_number')


@admin.action(description='Set Avtomat Max Sum')
def set_max_sum(modeladmin, request, queryset):
    avtomat_numbers = [item.avtomat_number for item in queryset]
    busy_avtomats = []
    command = '055be4'
    max_sum_hex_value = f"{Setting.objects.get(name='avtomat_max_sum').value:04x}"
    parameter = f'{command}00{max_sum_hex_value[2:]}{max_sum_hex_value[:2]}'
    for number in avtomat_numbers:
        busy_avtomat_number = set_param_for_avtomat(number, parameter)
        if busy_avtomat_number:
            busy_avtomats.append(busy_avtomat_number)
    if not busy_avtomats:
        messages.info(request, 'The maximum sum for avtomats was set')
    else:
        if len(busy_avtomats) == 1:
            messages.warning(request, f'Avtomat {busy_avtomats[0]} is busy!')
        else:
            messages.warning(request, f"Avtomats {', '.join(str(item) for item in busy_avtomats)} are busy!")


@admin.action(description='Set Avtomat Price')
def set_price(modeladmin, request, queryset):
    try:
        price = Setting.objects.get(name='avtomat_price').value
        queryset.update(price=int(price))
        messages.info(request, f"Avtomat's Price changed to {price / 100:.2f}")
    except Setting.DoesNotExist:
        messages.warning(request, 'You have to set "avtomat_price" in setting table')


@admin.action(description='Set Avtomat Price for App')
def set_price_for_app(modeladmin, request, queryset):
    try:
        price_for_app = Setting.objects.get(name='avtomat_price_for_app').value
        queryset.update(price_for_app=int(price_for_app))
        messages.info(request, f"Avtomat's Price for App changed to {price_for_app / 100:.2f}")
    except:
        messages.warning(request, 'You have to set "avtomat_price_for_app" in setting table')


@admin.action(description='Disable Avtomat Online Pay')
def disable_online_pay(modeladmin, request, queryset):
    queryset.update(price_for_app=None)
    messages.info(request, "Online Payments have been disabled for the selected machines")
