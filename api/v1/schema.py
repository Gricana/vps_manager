from django.conf import settings
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from api.v1.serializers import VPSSerializer

schema_view = get_schema_view(
    openapi.Info(
        title="VPS API",
        default_version="v1",
        description=_("VPS API"),
        contact=openapi.Contact(email="example@gmail.com"),
    ),
    public=True,
)

# Параметры фильтров для списка VPS
list_vps_parameters = [
    openapi.Parameter(
        "uid",
        openapi.IN_QUERY,
        description=_("UID VPS"),
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "ram",
        openapi.IN_QUERY,
        description=_("RAM Filter (GB)"),
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        "hdd",
        openapi.IN_QUERY,
        description=_("HDD Filter (GB)"),
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        "cpu",
        openapi.IN_QUERY,
        description=_("CPU core number filter"),
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        "status",
        openapi.IN_QUERY,
        description=_("VPS status filter"),
        type=openapi.TYPE_STRING,
        enum=["started", "blocked", "stopped"],
    ),
]

# Документация для списка VPS
list_vps_schema = {
    "operation_description": _("Get list VPS servers and filter"),
    "operation_id": "list_vps_servers",
    "manual_parameters": list_vps_parameters,
    "responses": {
        200: openapi.Response(
            description=_("Server list"),
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "servers": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "uid": openapi.Schema(type=openapi.TYPE_STRING),
                                "cpu": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "ram": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "hdd": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "status": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    ),
                },
            ),
        ),
        400: openapi.Response(
            description=_("Filter error"),
            examples={
                "application/json": {
                    "ram": [_("Enter a number.")],
                    "status": [
                        _(
                            "Select a valid choice. {reserved} is not one of the available choices."
                        )
                    ],
                }
            },
        ),
    },
}

# Документация для частичного обновления VPS
partial_update_vps_schema = {
    "operation_description": _("Update VPS status"),
    "operation_id": "partial_update_vps_server",
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=_("VPS status"),
                enum=["started", "stopped", "blocked"],
            ),
        },
        required=[],
    ),
    "responses": {
        200: openapi.Response(
            description=_("Success VPS updated status"),
            schema=VPSSerializer,
        ),
        400: openapi.Response(
            description=_("Validation error"),
            examples={
                "application/json": {
                    "status": [
                        _(
                            "Invalid status. Please select a valid option from (started, stopped, blocked)."
                        )
                    ],
                }
            },
        ),
        404: openapi.Response(
            description=_("Server not found"),
            examples={"application/json": {"detail": _("Not found.")}},
        ),
    },
}

# Документация для создания VPS
create_vps_schema = {
    "operation_description": _("Create VPS with specified parameters"),
    "operation_id": "create_vps_server",
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "ram": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description=_("RAM size (GB)"),
                minimum=settings.VPS_SETTINGS["RAM"]["MIN"],
                maximum=settings.VPS_SETTINGS["RAM"]["MAX"],
            ),
            "hdd": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description=_("HDD size (GB)"),
                minimum=settings.VPS_SETTINGS["HDD"]["MIN"],
                maximum=settings.VPS_SETTINGS["HDD"]["MAX"],
            ),
            "cpu": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description=_("CPU core number"),
                minimum=settings.VPS_SETTINGS["CPU"]["MIN"],
                maximum=settings.VPS_SETTINGS["CPU"]["MAX"],
            ),
            "status": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=_("VPS status"),
                enum=["started", "stopped", "blocked"],
            ),
        },
        required=["ram", "hdd", "cpu", "status"],
    ),
    "responses": {
        201: openapi.Response(
            description=_("Success VPS created"),
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "uid": openapi.Schema(type=openapi.TYPE_STRING),
                    "ram": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "hdd": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "cpu": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "status": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            examples={
                "application/json": {
                    "uid": "123e4567-e89b-12d3-a456-426614174000",
                    "ram": 16,
                    "hdd": 100,
                    "cpu": 4,
                    "status": "started",
                }
            },
        ),
        400: openapi.Response(
            description="Ошибка валидации данных",
            examples={
                "application/json": {
                    "cpu": [_("Ensure this value is less than or equal to 80.")],
                    "ram": [_("Ensure this value is greater than or equal to 2.")],
                    "hdd": [_("Ensure this value is greater than or equal to 5.")],
                    "status": [
                        _(
                            "Invalid status. Please select a valid option from (started, stopped, blocked)."
                        )
                    ],
                }
            },
        ),
    },
}
