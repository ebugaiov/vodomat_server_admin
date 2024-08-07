from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

from .models import Route


class InactiveAvtomatsListFilter(admin.SimpleListFilter):
    title = _('activity status')
    parameter_name = 'activity_status'

    def lookups(self, request, model_admin):
        return [
            ('inactive', _('Inactive'))
        ]

    def queryset(self, request, queryset):
        if self.value() == 'inactive':
            return queryset.filter(statistic_count=0)
        return queryset
    

class RoutesListFilter(admin.SimpleListFilter):
    title = _('route number')
    parameter_name = 'route_number'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        existing_lookups = [(obj.pk, obj.name) for obj in Route.objects.all()]
        extended_lookups = [('no_route', _('No route')), ] + existing_lookups
        return extended_lookups
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == 'no_route':
            return queryset.filter(route_id__isnull=True)
        elif self.value():
            return queryset.filter(route_id=self.value())
        return queryset
