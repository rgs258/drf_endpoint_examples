from django.db import IntegrityError, DataError
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet


# The names of actions that are performed in the context of a known object. These
# actions will engage the has_object_permission method on a Permission Class
VIEW_ACTIONS_KNOWN_OBJECT = (
    "retrieve",
    "update",
    "partial_update",
    "destroy",
)

# The names of actions that are performed on an object but without knowing about the
# object before beginning the action. These actions will NOT engage the
# has_object_permission method on a Permission Class. As a result, the has_permission
# method of the Permission Class needs to handle these with care else they'll get
# right through.
VIEW_ACTIONS_UNKNOWN_OBJECT = ("create",)

# The names of actions that are performed on any single object. Actions not in this
# list might be list actions.
# Please see https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
# for a discussion on view actions.
VIEW_ACTIONS_ANY_OBJECT = (*VIEW_ACTIONS_KNOWN_OBJECT, *VIEW_ACTIONS_UNKNOWN_OBJECT)


class ObjectIDRenderer(JSONRenderer):
    media_type = "text/plain; format=id"
    format = "txt"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            response = f"{data['id']}".encode()
        except Exception as e:
            response = super().render(data, accepted_media_type, renderer_context)
        return response


class ErrorExposingReadUpdateModelMixin:
    def reverse_action(self, url_name, *args, **kwargs):
        return super().reverse_action(url_name, *args, **kwargs)

    def get_renderers(self):
        renderers = super().get_renderers()
        if self.action in VIEW_ACTIONS_ANY_OBJECT:
            renderers = [ObjectIDRenderer(), *renderers]
        return renderers

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except (IntegrityError, DataError) as e:
            raise ValidationError(detail=e) from e

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ErrorExposingModelViewSet(ErrorExposingReadUpdateModelMixin, ModelViewSet):
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except (IntegrityError, DataError) as e:
            raise ValidationError(detail=e) from e

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except (IntegrityError, DataError) as e:
            raise ValidationError(detail=e) from e
