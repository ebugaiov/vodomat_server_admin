from django.db import models


class User(models.Model):
    username = models.CharField(unique=True, max_length=64)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    email = models.CharField(max_length=120, blank=True, null=True)
    password_hash = models.CharField(max_length=128)
    permission = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    last_visit = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
        ordering = ['username']

    def __str__(self):
        return self.username


class City(models.Model):
    city = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.city

