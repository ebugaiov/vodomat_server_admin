from typing import Optional
import redis
from django.contrib import admin, messages
from django.conf import settings
from .models import Setting


def set_param_redis(redis_con: redis.Redis, avtomat_number: int, param: str) -> Optional[int]:
    transaction, status = redis_con.hmget(avtomat_number, ['transaction', 'status'])
    if status == '1':
        return avtomat_number
    if transaction and int(transaction) < 999:
        transaction = int(transaction) + 1
    else:
        transaction = 1
    redis_con.hmset(avtomat_number, {'transaction': transaction, 'param': param})


@admin.action(description='Set Avtomat Max Sum')
def set_max_sum(modeladmin, request, queryset):
    avtomat_numbers = [item.avtomat_number for item in queryset]
    busy_avtomats = []
    command = '055be4'
    max_sum_hex_value = f"{Setting.objects.get(name='avtomat_max_sum').value:04x}"
    parameter = f'{command}00{max_sum_hex_value[2:]}{max_sum_hex_value[:2]}'
    with redis.Redis(host=settings.REDIS_HOST, charset='utf-8', decode_responses=True) as redis_con:
        for number in avtomat_numbers:
            busy_avtomat_number = set_param_redis(redis_con, number, parameter)
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
