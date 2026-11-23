import unittest
from unittest.mock import MagicMock, patch
from src.validator import TriangleValidator
from src.database import TriangleDatabase
from src.user_io import ConsoleUserIO
from src.controller import TriangleController


class TestUnit(unittest.TestCase):
    def test_validator_invalid(self):
        t, err = TriangleValidator.determine_type(1, 2, 10)
        self.assertIsNone(t)
        self.assertIn("не существует", err)

    def test_database_crud(self):
        db = TriangleDatabase(":memory:")
        db.add_record(3, 4, 5, "разносторонний", None)
        self.assertEqual(db.get_record(3, 4, 5)["triangle_type"], "разносторонний")
        self.assertTrue(db.delete_record(3, 4, 5))
        db.close()

    @patch("builtins.input", side_effect=["3", "3", "3"])
    def test_controller_with_mocks(self, mock_input):
        """Тест изоляции: подменяем input() и внешнюю зависимость"""
        db = TriangleDatabase(":memory:")
        notifier_mock = MagicMock()
        controller = TriangleController(ConsoleUserIO(), db, notifier_mock)

        result = controller.process()

        self.assertEqual(result["triangle_type"], "равносторонний")
        notifier_mock.send.assert_called_once()
        db.close()