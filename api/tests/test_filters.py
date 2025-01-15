from django.test import TestCase

from api.models import VPS
from api.v1.filters import VPSFilter


class VPSFilterTestCase(TestCase):
    """
    Тесты для проверки фильтров VPSFilter.
    """

    def setUp(self):
        """
        Устанавливает тестовые данные для тестов.
        Создаются 3 экземпляра модели VPS с различными параметрами.
        """
        VPS.objects.create(cpu=8, ram=32, hdd=500, status="started")
        VPS.objects.create(cpu=16, ram=64, hdd=1000, status="stopped")
        VPS.objects.create(cpu=4, ram=16, hdd=200, status="started")

    def test_filter_by_ram(self):
        """
        Тест фильтрации по параметру RAM.
        Проверяется, что фильтр возвращает только записи с указанным значением RAM.
        """
        queryset = VPS.objects.all()
        filter_set = VPSFilter({"ram": 32}, queryset=queryset)
        self.assertEqual(filter_set.qs.count(), 1)

    def test_filter_by_status(self):
        """
        Тест фильтрации по параметру статуса.
        Проверяется, что фильтр возвращает записи только с указанным статусом.
        """
        queryset = VPS.objects.all()
        filter_set = VPSFilter({"status": "started"}, queryset=queryset)
        self.assertEqual(filter_set.qs.count(), 2)

    def test_filter_by_multiple_fields(self):
        """
        Тест фильтрации по нескольким параметрам.
        Проверяется, что фильтр возвращает только записи, удовлетворяющие всем параметрам.
        """
        queryset = VPS.objects.all()
        filter_set = VPSFilter({"ram": 64, "status": "stopped"}, queryset=queryset)
        self.assertEqual(filter_set.qs.count(), 1)

    def test_filter_by_multiple_fields_with_error_values(self):
        """
        Тест фильтрации с некорректным значением для одного из параметров.
        Проверяется, что фильтр возвращает пустой результат или корректно обрабатывает ошибочные значения.
        """
        queryset = VPS.objects.all()
        filter_set = VPSFilter({"status": "reserved", "ram": 32}, queryset=queryset)
        self.assertEqual(
            filter_set.qs.count(), 0
        )  # Исправлено, результат должен быть пустым
