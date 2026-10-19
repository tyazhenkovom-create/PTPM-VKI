# -*- coding: utf-8 -*-
"""
Юнит-тесты для модуля расчета доставки delivery.py (Лабораторная работа №2).

Восстановленные бизнес-требования (по коду и docstring):
  * вес посылки: от 0.1 до 50.0 кг включительно;
  * расстояние: от 1 до 5000 км включительно;
  * тип посылки: "обычный", "хрупкий", "опасный";
  * базовая стоимость: 200 руб. + 5 руб. за каждый км;
  * весовой коэффициент: (>5 и <20 кг) -> x1.2, (>=20 кг) -> x1.5;
  * надбавка за тип: "хрупкий" +300 руб., "опасный" +1000 руб.;
  * экспресс-доставка - УСКОРЕНИЕ, т.е. удорожание (x1.5), а не скидка,
    и сокращение срока вдвое, но не менее чем до 1 дня;
  * срок: max(1, расстояние // 500) дней от даты отправки 2026-09-03;
  * при неверных параметрах возвращается (-1, "0000-00-00").
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from delivery import calculate_delivery_cost

BASE_DATE = "2026-09-03"  # фиксированная дата отправки в модуле


def shift_date(days: int) -> str:
    """Опорная дата доставки через N дней после отправки (без учета экспресса)."""
    import datetime
    d = datetime.date(2026, 9, 3) + datetime.timedelta(days=days)
    return d.strftime("%Y-%m-%d")


class TestDeliveryValidation(unittest.TestCase):
    """Проверка валидации входных параметров."""

    def test_weight_below_minimum_is_rejected(self):
        cost, date = calculate_delivery_cost(0.09, 100, "обычный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_min_valid_weight_is_accepted(self):
        cost, date = calculate_delivery_cost(0.1, 1, "обычный")
        self.assertEqual(cost, 205)
        self.assertNotEqual(date, "0000-00-00")

    def test_max_valid_weight_is_accepted(self):
        cost, _ = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertGreater(cost, 0)

    def test_weight_above_maximum_is_rejected(self):
        cost, date = calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_zero_distance_is_rejected(self):
        cost, date = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_distance_above_maximum_is_rejected(self):
        cost, date = calculate_delivery_cost(1.0, 5001, "обычный")
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_max_valid_distance_is_accepted(self):
        cost, date = calculate_delivery_cost(1.0, 5000, "обычный")
        self.assertEqual(cost, 25200)
        self.assertEqual(date, shift_date(10))

    def test_invalid_package_type_is_rejected(self):
        cost, date = calculate_delivery_cost(1.0, 100, "ледяной")
        self.assertEqual((cost, date), (-1, "0000-00-00"))


class TestDeliveryBaseCost(unittest.TestCase):
    """Проверка базового тарифа и весовых коэффициентов."""

    def test_base_cost_formula(self):
        # 200 + 100 * 5 = 700
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_medium_weight_applies_coefficient_1_2(self):
        # 700 * 1.2 = 840
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_heavy_weight_applies_coefficient_1_5(self):
        # 700 * 1.5 = 1050
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_light_weight_has_no_coefficient(self):
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 700)


class TestDeliveryPackageType(unittest.TestCase):
    """Проверка надбавок за тип посылки."""

    def test_fragile_package_adds_300_rubles(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_package_adds_1000_rubles(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 1700)


class TestDeliveryExpress(unittest.TestCase):
    """Проверка логики экспресс-доставки (ускорение = дороже и быстрее)."""

    def test_express_increases_cost(self):
        # 700 * 1.5 = 1050, а не 700 * 0.5 = 350
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertEqual(cost, 1050)

    def test_express_is_not_applied_by_default(self):
        cost_default, _ = calculate_delivery_cost(1.0, 100, "обычный")
        cost_explicit, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=False)
        self.assertEqual(cost_default, cost_explicit)

    def test_express_never_delivers_same_day(self):
        # даже на короткой дистанции доставка занимает минимум 1 день
        _, date = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertNotEqual(date, BASE_DATE)
        self.assertEqual(date, shift_date(1))

    def test_express_halves_delivery_time(self):
        # 3000 км: обычно 6 дней, экспресс - 3 дня
        _, date_normal = calculate_delivery_cost(1.0, 3000, "обычный")
        _, date_express = calculate_delivery_cost(1.0, 3000, "обычный", is_express=True)
        self.assertEqual(date_normal, shift_date(6))
        self.assertEqual(date_express, shift_date(3))


class TestDeliveryTerms(unittest.TestCase):
    """Проверка расчета сроков доставки."""

    def test_short_distance_takes_at_least_one_day(self):
        _, date = calculate_delivery_cost(1.0, 1, "обычный")
        self.assertEqual(date, shift_date(1))

    def test_distance_500km_takes_one_day(self):
        # 500 // 500 = 1 день (граница диапазона)
        _, date = calculate_delivery_cost(1.0, 500, "обычный")
        self.assertEqual(date, shift_date(1))

    def test_distance_2500km_takes_five_days(self):
        _, date = calculate_delivery_cost(1.0, 2500, "обычный")
        self.assertEqual(date, shift_date(5))

    def test_delivery_date_format_is_iso(self):
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")


class TestDeliveryReturnTypesAndCombo(unittest.TestCase):
    """Проверка типов возвращаемых значений и комбинированного расчета."""

    def test_returned_types_are_int_and_str(self):
        cost, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertIsInstance(cost, int)
        self.assertIsInstance(date, str)

    def test_combined_heavy_fragile_express_cost(self):
        # (200 + 100*5) * 1.5 + 300 = 1350; * 1.5 (экспресс) = 2025
        cost, _ = calculate_delivery_cost(25.0, 100, "хрупкий", is_express=True)
        self.assertEqual(cost, 2025)

    def test_max_weight_max_distance_accepted(self):
        cost, date = calculate_delivery_cost(50.0, 5000, "опасный")
        self.assertEqual(cost, (200 + 5000 * 5) * 1.5 + 1000)  # = 38800
        self.assertEqual(date, shift_date(10))


if __name__ == "__main__":
    unittest.main()