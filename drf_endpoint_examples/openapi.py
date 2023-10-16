import logging
from collections import OrderedDict
from decimal import Decimal
from operator import attrgetter

from django_filters.rest_framework import DjangoFilterBackend, BooleanFilter
from rest_framework import parsers
from rest_framework.fields import MultipleChoiceField, ChoiceField
from rest_framework.schemas.openapi import SchemaGenerator, AutoSchema

from drf_endpoint_examples.drf import IntegerFilter

logger = logging.getLogger(__name__)


class ChoicesDjangoFilterBackend(DjangoFilterBackend):
    def get_schema_operation_parameters(self, view):
        try:
            queryset = view.get_queryset()
        except Exception:
            queryset = None
            logger.warning(
                "{} is not compatible with schema generation".format(view.__class__)
            )

        filterset_class = self.get_filterset_class(view, queryset)

        if not filterset_class:
            return []

        parameters = []
        for field_name, field in filterset_class.base_filters.items():
            # choices code loosely taken from
            # rest_framework.schemas.openapi.AutoSchema.map_choicefield
            choices_type = "string"
            if isinstance(field, BooleanFilter):
                choices_type = "boolean"
            elif isinstance(field, IntegerFilter):
                choices_type = "integer"
            elif hasattr(field.field, "choices"):
                choices = list(OrderedDict(field.field.choices))
                if all((isinstance(choice, bool) or not choice) for choice in choices):
                    choices_type = "boolean"
                elif all((isinstance(choice, int) or not choice) for choice in choices):
                    choices_type = "integer"
                elif all(
                    (isinstance(choice, (int, float, Decimal)) or not choice)
                    for choice in choices
                ):  # `number` includes `integer`
                    choices_type = "number"
                elif all(isinstance(choice, str) for choice in choices):
                    choices_type = "string"
            elif field.field.widget.input_type in (
                "string",
                "number",
                "integer",
                "boolean",
                "array",
                "object",
            ):
                choices_type = field.field.widget.input_type

            parameter = {
                "name": field_name,
                "required": field.extra["required"],
                "in": "query",
                "description": field.label if field.label is not None else field_name,
                "schema": {
                    "type": choices_type,
                },
            }

            if field.extra and "choices" in field.extra:
                parameter["schema"]["enum"] = [c[0] for c in field.extra["choices"]]
                parameter["description"] += " \n\n Choices: \n* " + "\n* ".join(
                    ["`{}` - {}".format(c[0], c[1]) for c in field.extra["choices"]]
                )
            parameters.append(parameter)

        return parameters


class BytestreamSerializerFlagMixin:
    """
    Add this mixin to a serializer to indicate to `ChoicesAutoSchema` that the response
    will be a bytestream.
    """


class ChoicesAutoSchema(AutoSchema):
    """
    An auto schema that adds the choices to the schema documentation.
    """

    parser_classes = [
        parsers.JSONParser,
    ]

    def map_parsers(self, path, method):
        if self.parser_classes:
            return list(map(attrgetter("media_type"), self.parser_classes))
        return super().map_parsers(path, method)

    def map_serializer(self, serializer):
        for field in serializer.fields.values():
            if isinstance(field, (MultipleChoiceField, ChoiceField)):
                field.help_text = getattr(field, "help_text", None) or ""
                field.help_text += " \n\n Choices: \n* " + "\n* ".join(
                    [
                        "`{}` - {}".format(key, value)
                        for key, value in field.choices.items()
                    ]
                )
        return super().map_serializer(serializer)

    def _get_reference(self, serializer):
        if isinstance(serializer, BytestreamSerializerFlagMixin):
            # While "string" is the correct openapi3 format, swaggger-codegen doesn't
            # deserialize string correctly so "file" type is maintained form openapi2
            return {"type": "file", "format": "binary"}
        else:
            return super()._get_reference(serializer)


class AuthSchemaGenerator(SchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)

        schema["security"] = [
            {"TokenAuthentication": []},
        ]

        schema["components"].update(
            {
                "securitySchemes": {
                    "TokenAuthentication": {
                        "type": "apiKey",
                        "in": "header",
                        "name": "Authorization",
                    }
                }
            }
        )
        return schema
