import unittest

from src.converter import Converter


class TestConverterDo(unittest.TestCase):
    """
    Полное покрытие метода Converter.do():
    все 5 диапазонов + границы + исключение.
    """

    # ---------- 1. x ∈ [100.7; +∞) -> 1000 ----------

    def test_upper_range_lower_boundary(self):
        """Граница: x == 100.7 -> 1000."""
        self.assertEqual(Converter.do(100.7), 1000)

    def test_upper_range_middle(self):
        """Внутри диапазона: x == 500.0 -> 1000."""
        self.assertEqual(Converter.do(500.0), 1000)

    def test_upper_range_large(self):
        """Очень большое значение: x == 1_000_000.0 -> 1000."""
        self.assertEqual(Converter.do(1_000_000.0), 1000)

    # ---------- 2. x ∈ (0; 100.7) -> int(x) ----------

    def test_positive_range_just_above_zero(self):
        """Только что выше нуля: x == 0.1 -> 0 (int(0.1) == 0)."""
        self.assertEqual(Converter.do(0.1), 0)

    def test_positive_range_middle(self):
        """Середина: x == 65.7 -> 65."""
        self.assertEqual(Converter.do(65.7), 65)

    def test_positive_range_truncates_fraction(self):
        """Проверка отбрасывания дробной части: x == 99.9 -> 99."""
        self.assertEqual(Converter.do(99.9), 99)

    def test_positive_range_upper_boundary_exclusive(self):
        """Чуть ниже верхней границы: x == 100.6 -> 100."""
        self.assertEqual(Converter.do(100.6), 100)

    # ---------- 3. x == 0.0 -> ValueError ----------

    def test_zero_raises_value_error(self):
        """Ровно ноль: должно быть исключение ValueError."""
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    def test_zero_raises_value_error_message(self):
        """Проверка, что исключение действительно ValueError (не подкласс случайный)."""
        with self.assertRaises(ValueError) as ctx:
            Converter.do(0.0)
        self.assertIsInstance(ctx.exception, ValueError)

    # ---------- 4. x ∈ [-30.4; 0) -> int(x) - 5 ----------

    def test_negative_range_upper_boundary(self):
        """Граница: x == -30.4 -> int(-30.4) - 5 == -30 - 5 == -35."""
        self.assertEqual(Converter.do(-30.4), -35)

    def test_negative_range_just_below_zero(self):
        """Чуть ниже нуля: x == -0.1 -> int(-0.1) - 5 == 0 - 5 == -5."""
        self.assertEqual(Converter.do(-0.1), -5)

    def test_negative_range_middle(self):
        """Середина: x == -15.5 -> int(-15.5) - 5 == -15 - 5 == -20."""
        self.assertEqual(Converter.do(-15.5), -20)

    def test_negative_range_truncates_toward_zero(self):
        """Проверка int() на отрицательных: x == -7.9 -> -7 - 5 == -12."""
        self.assertEqual(Converter.do(-7.9), -12)

    # ---------- 5. x ∈ (-∞; -30.5] -> -2000 ----------

    def test_lower_range_boundary(self):
        """Граница: x == -30.5 -> -2000."""
        self.assertEqual(Converter.do(-30.5), -2000)

    def test_lower_range_middle(self):
        """Внутри: x == -94.5 -> -2000."""
        self.assertEqual(Converter.do(-94.5), -2000)

    def test_lower_range_large_negative(self):
        """Очень маленькое значение: x == -1_000_000.0 -> -2000."""
        self.assertEqual(Converter.do(-1_000_000.0), -2000)


if __name__ == "__main__":
    unittest.main()