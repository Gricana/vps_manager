from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from api.models import VPS


class VPSFilter(filters.FilterSet):
    """
    Фильтр для модели VPS.
    Позволяет выполнять фильтрацию по следующим параметрам:
    - RAM (оперативная память)
    - HDD (дисковое пространство)
    - CPU (количество ядер процессора)
    - Status (текущий статус сервера)
    """

    ram = filters.NumberFilter(
        field_name="ram",
        lookup_expr="exact",
        label=_("RAM (GB)"),
        help_text=_("Фильтрация по точному значению объёма оперативной памяти (в ГБ)."),
    )
    hdd = filters.NumberFilter(
        field_name="hdd",
        lookup_expr="exact",
        label=_("HDD (GB)"),
        help_text=_(
            "Фильтрация по точному значению объёма дискового пространства (в ГБ)."
        ),
    )
    cpu = filters.NumberFilter(
        field_name="cpu",
        lookup_expr="exact",
        label=_("Number CPU cores"),
        help_text=_("Фильтрация по точному значению количества ядер процессора."),
    )
    status = filters.ChoiceFilter(
        choices=VPS.STATUS_CHOICES,
        label=_("Status"),
        help_text=_("Фильтрация по статусу сервера."),
    )

    class Meta:
        model = VPS
        fields = "__all__"
