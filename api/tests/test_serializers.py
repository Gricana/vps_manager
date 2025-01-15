from django.test import TestCase

from api.v1.serializers import VPSSerializer


class VPSSerializerTestCase(TestCase):
    """
    Набор тестов для проверки корректности работы сериализатора VPSSerializer.
    """

    def setUp(self):
        """
        Устанавливает тестовые данные для проверки сериализатора.
        """
        self.valid_data = {
            "uid": "123e4567-e89b-12d3-a456-426614174000",
            "cpu": 8,
            "ram": 32,
            "hdd": 100,
            "status": "started",
        }
        self.invalid_size_data = {
            "uid": "123e4567-e89b-12d3-a456-426614174000",
            "cpu": 8,
            "ram": 320,  # Превышает максимальное значение
            "hdd": -100,  # Отрицательное значение
            "status": "started",
        }
        self.invalid_data = {
            "cpu": 8,
            "ram": 31,  # Нечетное значение
            "hdd": 100,
            "status": "reserved",  # Недопустимый статус
        }

    def test_valid_data(self):
        """
        Проверяет, что сериализатор корректно обрабатывает валидные данные.
        """
        serializer = VPSSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data["ram"], 32
        )  # Убедиться, что RAM остаётся без изменений

    def test_invalid_status(self):
        """
        Проверяет, что сериализатор возвращает ошибку для недопустимого статуса.
        """
        serializer = VPSSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)
        self.assertEqual(
            serializer.errors["status"][0],
            "Невалидный статус. Пожалуйста, выберите из списка ('started', 'stopped', 'blocked')",
        )

    def test_invalid_size(self):
        """
        Проверяет, что сериализатор возвращает ошибки для некорректных значений RAM и HDD.
        """
        serializer = VPSSerializer(data=self.invalid_size_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("ram", serializer.errors)  # Проверяет ошибку для RAM
        self.assertIn("hdd", serializer.errors)  # Проверяет ошибку для HDD
        self.assertEqual(
            str(serializer.errors["ram"][0]),
            "Убедитесь, что это значение меньше либо равно 64.",
        )
        self.assertEqual(
            serializer.errors["hdd"][0],
            "Убедитесь, что это значение больше либо равно 5.",
        )

    def test_ram_adjustment(self):
        """
        Проверяет, что нечётное значение RAM автоматически корректируется на чётное.
        """
        data = self.valid_data.copy()
        data["ram"] = 33  # Нечётное значение
        serializer = VPSSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(
            serializer.validated_data["ram"], 32
        )  # RAM округляется до ближайшего чётного
