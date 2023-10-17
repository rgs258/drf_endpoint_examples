# Register your models here.

from django.contrib import admin
from django.utils.safestring import mark_safe
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import TokenProxy

from .models import Customer, Product, Order, Address, Review

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Review)


class ExtendedTokenAdmin(TokenAdmin):
    readonly_fields = ("created",)
    list_display = ("key", "user", "created")
    fields = None
    fieldsets = (
        (
            None,
            {
                "fields": ("key", "user", "created"),
                "description": mark_safe(
                    "There is no Change permission; please instead delete, and then "
                    "re-add, the `Token`."
                ),
            },
        ),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if form.base_fields.get("key", None):
            form.base_fields["key"].initial = TokenProxy.generate_key()
        return form

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# unregister and register again
admin.site.unregister(TokenProxy)
admin.site.register(TokenProxy, ExtendedTokenAdmin)
