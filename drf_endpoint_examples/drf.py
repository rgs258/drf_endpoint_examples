import typing

from django import forms
from django.http import HttpRequest
from django_filters import Filter
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser


class AllVerbDjangoModelPermissions(DjangoModelPermissions):
    """
    Same as superclass but implements view permissions, and blocks objects.
    """
    perms_map = {
        'GET': ["%(app_label)s.view_%(model_name)s"],
        'OPTIONS': ["%(app_label)s.view_%(model_name)s"],
        'HEAD': ["%(app_label)s.view_%(model_name)s"],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_object_permission(
        self, request: HttpRequest, view: typing.Any, obj: typing.Any
    ) -> bool:
        return self.has_permission(request, view)


class ObjectIsAdminUser(IsAdminUser):
    """
    Like its superclass, but blocks objects too
    """

    def has_object_permission(
        self, request: HttpRequest, view: typing.Any, obj: typing.Any
    ) -> bool:
        return self.has_permission(request, view)


class IntegerFilter(Filter):
    field_class = forms.IntegerField
