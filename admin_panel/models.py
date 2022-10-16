from django.db import models
from django.utils.html import format_html


class User(models.Model):
    USER_PERMISSION = (
        ('admin', 'Administrator'),
        ('operator', 'Operator'),
        ('driver', 'Driver'),
        ('api', 'API')
    )

    username = models.CharField(unique=True, max_length=64)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    email = models.CharField(max_length=120, blank=True, null=True)
    password_hash = models.CharField(max_length=128)
    permission = models.CharField(
        max_length=64, choices=USER_PERMISSION, default='operator')
    city = models.CharField(max_length=64, blank=True, null=True)
    last_visit = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
        ordering = ['username']

    def __str__(self):
        return self.username


class Route(models.Model):
    name = models.CharField(max_length=16)
    car_number = models.CharField(max_length=16, blank=True, null=True)
    driver_1 = models.CharField(max_length=32, blank=True, null=True)
    driver_2 = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'route'
        ordering = ['name']

    def __str__(self):
        return f'{self.car_number} ({self.name})'


class City(models.Model):
    city = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'city'
        ordering = ['city']
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.city


class Street(models.Model):
    street = models.CharField(max_length=64)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'street'
        ordering = ['street']

    def __str__(self):
        return self.street


class Avtomat(models.Model):
    SIZE = (
        (470, 'Single'),
        (940, 'Double'),
        (471, 'Double/1')
    )
    COMPETITORS = (
        (0, 'No'),
        (1, 'Yes')
    )
    STATE = (
        (0, 'Undefined'),
        (1, 'Normal'),
        (2, 'No Volt'),
        (3, 'Crashed')
    )
    PAYMENT_GATEWAY_NAME = (
        ('portmone', 'Portmone'),
        ('monobank', 'Monobank')
    )
    SECURITY_STATE = (
        (None, 'No Security'),
        (1, 'Security ON'),
        (2, 'Security OFF'),
        (3, 'Undefined'),
    )
    avtomat_number = models.AutoField(primary_key=True)
    house = models.CharField(max_length=16, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    search_radius = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    price_for_app = models.IntegerField(blank=True, null=True)
    payment_app_url = models.CharField(max_length=64, blank=True, null=True)
    payment_gateway_name = models.CharField(max_length=64, blank=True, null=True, choices=PAYMENT_GATEWAY_NAME)
    payment_gateway_url = models.CharField(
        max_length=64, blank=True, null=True)
    max_sum = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(
        choices=SIZE, blank=True, null=True, default=470)
    competitors = models.IntegerField(
        choices=COMPETITORS, blank=True, null=True, default=0)
    state = models.IntegerField(choices=STATE, blank=True, null=True)
    route = models.ForeignKey(
        'Route', models.DO_NOTHING, blank=True, null=True)
    street = models.ForeignKey(
        'Street', models.DO_NOTHING, blank=True, null=True)
    rro_id = models.CharField(max_length=9, blank=True, null=True, verbose_name='RRO ID')
    security_id = models.CharField(max_length=9, blank=True, null=True, verbose_name='Security ID')
    security_state = models.IntegerField(
        choices=SECURITY_STATE, blank=True, null=True, verbose_name='Security State')

    class Meta:
        managed = False
        db_table = 'avtomat'
        ordering = ['avtomat_number']

    def __str__(self):
        return f'New {self.avtomat_number}' if self.house is None else f'Avtomat {self.avtomat_number}'
