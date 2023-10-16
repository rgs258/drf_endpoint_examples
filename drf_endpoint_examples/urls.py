"""
URL configuration for drf_endpoint_examples project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from drf_endpoint_examples.openapi import AuthSchemaGenerator
from endpoints.viewsets import (
    CustomerViewSet,
    ProductViewSet,
    OrderViewSet,
    AddressViewSet,
    ReviewViewSet,
)

display_name = "DRF Endpoint Examples"


router = routers.DefaultRouter()
router.register(r"customers", CustomerViewSet)
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"addresses", AddressViewSet)
router.register(r"reviews", ReviewViewSet)

schema_url_patterns = [path(f"api/", include(router.urls))]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path(
        "openapi/",
        staff_member_required(
            get_schema_view(
                title=display_name,
                description=f"Swagger API Documentation for {display_name}.",
                version="1.0.0",
                patterns=schema_url_patterns,
                generator_class=AuthSchemaGenerator,
            )
        ),
        name="openapi-schema",
    ),
    path(
        "swagger-ui/",
        staff_member_required(
            TemplateView.as_view(
                template_name="swagger-ui.html",
                extra_context={
                    "schema_url": f"openapi-schema",
                    "api_name": display_name,
                    "api_swagger_url": f"swagger-ui",
                },
            )
        ),
        name="swagger-ui",
    ),
]
