from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.models import VPS


class VPSSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели VPS.
    """

    class Meta:
        """
        Метаданные сериализатора.
        Указывает модель, поля и дополнительные параметры для обработки ошибок.
        """

        model = VPS
        fields = "__all__"
        extra_kwargs = {
            "status": {
                "error_messages": {
                    "invalid_choice": _(
                        f"Invalid status. Please select a valid option from ({VPS.get_status_choices()})."
                    ),
                },
            },
        }

    def validate_ram(self, value):
        """
        Кастомная валидация для поля RAM.
        Проверяет, что значение RAM является чётным числом.
        Если значение нечётное, оно округляется вниз до ближайшего чётного числа.

        :param value: Значение RAM
        :return: Откорректированное значение RAM
        """
        if value % 2 != 0:
            value -= 1
        return value
