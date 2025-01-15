import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class VPS(models.Model):
    """
    Модель для представления виртуального сервера (VPS).
    Хранит информацию о количестве CPU, оперативной памяти (RAM),
    объёме диска (HDD) и статусе сервера.
    """

    STATUS_CHOICES = (
        ("started", _("Started")),  # Сервер запущен
        ("stopped", _("Stopped")),  # Сервер остановлен
        ("blocked", _("Blocked")),  # Сервер заблокирован
    )

    uid = models.UUIDField(
        verbose_name=_("UUID"),
        primary_key=True,
        default=uuid.uuid4,
    )
    cpu = models.PositiveIntegerField(
        verbose_name=_("CPU"),
        validators=[
            MinValueValidator(settings.VPS_SETTINGS["CPU"]["MIN"]),
            MaxValueValidator(settings.VPS_SETTINGS["CPU"]["MAX"]),
        ],
    )
    ram = models.PositiveIntegerField(
        verbose_name=_("RAM (Gb)"),
        validators=[
            MinValueValidator(settings.VPS_SETTINGS["RAM"]["MIN"]),
            MaxValueValidator(settings.VPS_SETTINGS["RAM"]["MAX"]),
        ],
    )  # In GB
    hdd = models.PositiveIntegerField(
        verbose_name=_("HDD (Gb)"),
        validators=[
            MinValueValidator(settings.VPS_SETTINGS["HDD"]["MIN"]),
            MaxValueValidator(settings.VPS_SETTINGS["HDD"]["MAX"]),
        ],
    )  # In GB
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[2][0],  # По умолчанию статус "Blocked"
    )

    @classmethod
    def get_status_choices(cls):
        """
        Возвращает строку с перечислением всех доступных статусов.

        :return: Строка с доступными статусами, разделёнными запятыми.
        """
        return ", ".join(choice[0] for choice in cls.STATUS_CHOICES)

    def __str__(self):
        """
        Возвращает строковое представление объекта VPS.

        :return: Строка вида "VPS #<UUID> - Status: <status>"
        """
        return f"VPS #{self.uid} - Status: {self.status}"

    class Meta:
        verbose_name = _("VPS")
        verbose_name_plural = _("VPSs")
        ordering = ("-status",)
