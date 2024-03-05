from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class InactiveAvtomatsListFilter(admin.SimpleListFilter):
    title = _('inactive avtomats')
    parameter_name = 'inactive_avtomats'

    def lookups(self, request, model_admin):
        return [
            ('inactive', _('Inactive'))
        ]

    def queryset(self, request, queryset):
        if self.value() == 'inactive':
            return queryset.filter(statistic_count=0)
        return queryset
