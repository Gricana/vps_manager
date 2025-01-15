from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from api.models import VPS


class VPSViewSetTestCase(TestCase):
    """
    Тесты для проверки работы ViewSet VPS.
    """

    def setUp(self):
        """
        Устанавливает тестовые данные для проверки API.
        """
        self.client = APIClient()
        self.vps = VPS.objects.create(cpu=8, ram=32, hdd=500, status="started")

        # Корректные и некорректные данные для тестов
        self.valid_data = {
            "cpu": 4,
            "ram": 17,  # Нечётное значение будет округлено
            "hdd": 100,
            "status": "stopped",
        }
        self.invalid_data = {
            "cpu": 4,
            "ram": 310,  # Превышает максимальный размер
            "hdd": 10000,  # Превышает максимальный размер
            "status": "invalid_status",  # Недопустимое значение статуса
        }
        self.list_vps = reverse("vps-list")

    def test_list_vps(self):
        """
        Тест получения списка VPS серверов.
        """
        response = self.client.get(self.list_vps)
        self.assertEqual(response.status_code, 200)
        self.assertIn("servers", response.data)

    def test_retrieve_vps(self):
        """
        Тест получения конкретного VPS по UID.
        """
        response = self.client.get(reverse("vps-detail", kwargs={"uid": self.vps.uid}))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_unknown_vps(self):
        """
        Тест получения несуществующего VPS по UID.
        """
        response = self.client.get(
            reverse("vps-detail", kwargs={"uid": "bfd1ca37-dc37-497c-97f1-8b9d98db884"})
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.json()["detail"], "Не найден сервер по указанному UID"
        )

    def test_create_vps(self):
        """
        Тест создания нового VPS с корректными данными.
        """
        response = self.client.post(self.list_vps, data=self.valid_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "stopped")
        self.assertEqual(
            response.data["ram"], 16
        )  # RAM округляется до ближайшего чётного

    def test_create_vps_invalid(self):
        """
        Тест создания VPS с некорректными данными.
        """
        response = self.client.post(
            self.list_vps, data=self.invalid_data, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("status", response.data)
        self.assertEqual(
            response.json()["ram"][0],
            "Убедитесь, что это значение меньше либо равно 64.",
        )
        self.assertEqual(
            response.json()["status"][0],
            "Невалидный статус. Пожалуйста, выберите из списка ('started', 'stopped', 'blocked')",
        )
        self.assertEqual(
            response.json()["hdd"][0],
            "Убедитесь, что это значение меньше либо равно 4096.",
        )

    def test_partial_update_vps(self):
        """
        Тест частичного обновления VPS (статус).
        """
        response = self.client.patch(
            reverse("vps-detail", kwargs={"uid": self.vps.uid}),
            data={"status": "stopped"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "stopped")

    def test_partial_update_invalid_status(self):
        """
        Тест частичного обновления VPS с некорректным статусом.
        """
        response = self.client.patch(
            reverse("vps-detail", kwargs={"uid": self.vps.uid}),
            data={"status": "reversed"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("status", response.data)
        self.assertEqual(
            response.json()["status"][0],
            "Невалидный статус. Пожалуйста, выберите из списка ('started', 'stopped', 'blocked')",
        )
