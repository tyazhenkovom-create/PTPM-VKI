import unittest
from unittest.mock import patch
from src.database import TriangleDatabase
from src.user_io import ConsoleUserIO
from src.notifier import ConsoleNotifier
from src.controller import TriangleController


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.db = TriangleDatabase(":memory:")
        self.notifier = ConsoleNotifier()
        self.controller = TriangleController(ConsoleUserIO(), self.db, self.notifier)

    def tearDown(self):
        self.db.close()

    def test_full_cycle_new(self):
        """Интеграция: ввод -> вычисление -> сохранение -> отправка"""
        with patch("builtins.input", side_effect=["3", "3", "3"]):
            result = self.controller.process()

        self.assertFalse(result["from_db"])
        self.assertEqual(result["triangle_type"], "равносторонний")
        self.assertIsNotNone(self.db.get_record(3, 3, 3))
        self.assertEqual(len(self.notifier.sent_messages), 1)

    def test_full_cycle_cached(self):
        """Интеграция: повторный ввод берет данные из БД (кэш)"""
        with patch("builtins.input", side_effect=["3", "4", "5"]):
            self.controller.process()
        with patch("builtins.input", side_effect=["3", "4", "5"]):
            result = self.controller.process()

        self.assertTrue(result["from_db"])
        self.assertEqual(result["triangle_type"], "разносторонний")
        self.assertEqual(len(self.notifier.sent_messages), 2)

    def test_full_cycle_error(self):
        """Интеграция: невалидные данные сохраняются с ошибкой"""
        with patch("builtins.input", side_effect=["1", "2", "10"]):
            result = self.controller.process()

        self.assertIsNone(result["triangle_type"])
        self.assertIn("не существует", self.db.get_record(1, 2, 10)["error_message"])
        self.assertEqual(len(self.notifier.sent_messages), 1)