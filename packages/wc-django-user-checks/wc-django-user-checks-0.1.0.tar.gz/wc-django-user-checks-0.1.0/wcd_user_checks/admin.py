from django.contrib import admin
from django import forms
from django.utils.translation import pgettext_lazy, gettext_lazy as _

from .cases import send_checks_changed
from .models import UserCheck
from .discovery import get_registry
from .utils import fix_check


__all__ = (
    'ReasonFilter',
    'StateFilter',
    'UserCheckAdminForm',
    'UserCheckInlineAdmin',
    'UserCheckAdmin',
)


class ReasonFilter(admin.ChoicesFieldListFilter):
    def choices(self, changelist):
        yield {
            'selected': self.lookup_val is None,
            'query_string': changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All')
        }
        none_title = ''
        for lookup, title in get_registry().choices:
            if lookup is None:
                none_title = title
                continue
            yield {
                'selected': str(lookup) == self.lookup_val,
                'query_string': changelist.get_query_string({self.lookup_kwarg: lookup}, [self.lookup_kwarg_isnull]),
                'display': title,
            }
        if none_title:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': changelist.get_query_string({self.lookup_kwarg_isnull: 'True'}, [self.lookup_kwarg]),
                'display': none_title,
            }


class StateFilter(admin.ChoicesFieldListFilter):
    def choices(self, changelist):
        registry = get_registry()
        reason = changelist.params.get('reason__exact')

        if not reason or reason not in registry:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': changelist.get_query_string({}, [self.lookup_kwarg]),
                'display': pgettext_lazy('wcd_user_checks:admin', 'Select reason first'),
            }

            return

        yield {
            'selected': self.lookup_val is None,
            'query_string': changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All')
        }
        none_title = ''
        for lookup, title in registry[reason].choices:
            if lookup is None:
                none_title = title
                continue
            yield {
                'selected': str(lookup) == self.lookup_val,
                'query_string': changelist.get_query_string({self.lookup_kwarg: lookup}, [self.lookup_kwarg_isnull]),
                'display': title,
            }
        if none_title:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': changelist.get_query_string({self.lookup_kwarg_isnull: 'True'}, [self.lookup_kwarg]),
                'display': none_title,
            }


class UserCheckAdminForm(forms.ModelForm):
    class Meta:
        model = UserCheck
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        registry = get_registry()

        if 'reason' in self.fields:
            self.fields['reason'].widget = forms.Select(
                choices = registry.choices
            )

        if 'state' in self.fields:
            reason = self.instance and self.instance.reason

            if reason and reason in registry:
                self.fields['state'].widget = forms.Select(
                    choices = registry[reason].choices
                )



class AdminBaseMixin:
    readonly_fields = (
        'user', 'reason', 'meta', 'is_passed', 'created_at', 'updated_at',
    )
    readonly_fields_on_create = ()

    def get_readonly_fields(self, request, obj = None):
        if obj is None:
            return self.readonly_fields_on_create

        return super().get_readonly_fields(request, obj=obj)

    def save_model(self, request, obj, form, change):
        obj = fix_check(get_registry(), obj)
        super().save_model(request, obj, form, change)
        send_checks_changed([obj])


class UserCheckInlineAdmin(AdminBaseMixin, admin.TabularInline):
    form = UserCheckAdminForm
    model = UserCheck
    extra = 0
    show_change_link = True
    readonly_fields = (
        'reason', 'state', 'message', 'is_passed', # 'meta', 'user', 'created_at', 'updated_at',
    )
    fields = readonly_fields

    def has_add_permission(self, request, obj):
        return False


@admin.register(UserCheck)
class UserCheckAdmin(AdminBaseMixin, admin.ModelAdmin):
    list_display = 'user', 'get_reason_display', 'get_state_display', 'is_passed'
    list_display_links = 'user', 'get_reason_display',
    list_filter = (
        'is_passed',
        'user',
        ('reason', ReasonFilter),
        ('state', StateFilter)
    )
    list_select_related = 'user',
    autocomplete_fields = 'user',
    search_fields = 'reason', 'state', 'message', 'user__username', 'meta',
    form = UserCheckAdminForm

    date_hierarchy = 'updated_at'

    fields_on_create = 'user', 'reason', 'message',
    fieldsets = (
        (None, {
            'fields': (
                ('user', 'reason',),
                'message',
            )
        }),
    )
    fieldsets_on_update = (
        (None, {
            'fields': (
                ('user', 'reason',),
                ('state', 'is_passed',),
                'message',
            )
        }),
        (pgettext_lazy('wcd_user_checks:admin', 'Dates'), {
            'classes': ('collapse',),
            'fields': (('created_at', 'updated_at'),),
        }),
        (pgettext_lazy('wcd_user_checks:admin', 'Metadata'), {
            'classes': ('collapse',),
            'fields': ('meta',),
        }),
    )

    def get_fields(self, request, obj=None):
        if obj is None and self.fields_on_create:
            return self.fields_on_create

        return super().get_fields(request, obj=obj)

    def get_fieldsets(self, request, obj = None):
        if obj is not None:
            return self.fieldsets_on_update

        return super().get_fieldsets(request, obj=obj)

    @admin.display(
        ordering='reason',
        description=UserCheck._meta.get_field('reason').verbose_name
    )
    def get_reason_display(self, obj):
        return obj.get_reason_display()

    @admin.display(
        ordering='state',
        description=UserCheck._meta.get_field('state').verbose_name
    )
    def get_state_display(self, obj):
        return obj.get_state_display()
