from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import VPS
from api.v1.filters import VPSFilter
from api.v1.schema import create_vps_schema, list_vps_schema, partial_update_vps_schema
from api.v1.serializers import VPSSerializer


class VPSViewSet(ModelViewSet):
    """
    ViewSet для управления объектами модели VPS.
    Предоставляет следующие действия:
    - Получение списка VPS (list)
    - Создание нового VPS (create)
    - Частичное обновление существующего VPS (partial_update)
    """

    http_method_names = ["get", "post", "patch", "options"]
    queryset = VPS.objects.all()
    serializer_class = VPSSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = VPSFilter
    lookup_field = "uid"

    @swagger_auto_schema(**list_vps_schema)
    def list(self, request, *args, **kwargs):
        """
        Получение списка всех VPS серверов с возможностью фильтрации.
        """
        servers = super().list(request, *args, **kwargs)
        return Response(data={"servers": servers.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(**create_vps_schema)
    def create(self, request, *args, **kwargs):
        """
        Создание нового VPS сервера на основе данных запроса.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(**partial_update_vps_schema)
    def partial_update(self, request, *args, **kwargs):
        """
        Частичное обновление данных существующего VPS.
        Поддерживает обновление поля статус у объекта VPS.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Обновление статуса, если он присутствует в данных
        if "status" in serializer.validated_data:
            instance.status = serializer.validated_data["status"]
            instance.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
