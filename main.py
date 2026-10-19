import logging
import sys
import os
import math


def setup_logger():
    """Настройка логирования в консоль и файл Logs/file_txt.log."""
    os.makedirs("Logs", exist_ok=True)

    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("Logs/file_txt.log", encoding="utf-8")
        ]
    )

    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")


def calculate_vertices(a: float, b: float, c: float):
    """Вычисляет координаты вершин треугольника и масштабирует их в поле 100x100 px.

    Вершина A -> (0, 0), B -> (a, 0), C -> (x, y).
    """
    # A = (0, 0), B = (c, 0). Точка C находится на пересечении окружностей
    # радиуса b (вокруг A) и радиуса a (вокруг B).
    x = (b * b + c * c - a * a) / (2 * c)
    y = math.sqrt(max(b * b - x * x, 0.0))

    # Масштабирование так, чтобы треугольник поместился в поле 100x100 px
    scale = 100.0 / max(a, b, c)
    vertices = [
        (int(round(0 * scale)), int(round(0 * scale))),
        (int(round(c * scale)), int(round(0 * scale))),
        (int(round(x * scale)), int(round(y * scale)))
    ]
    return vertices


def get_triangle_type(str_a: str, str_b: str, str_c: str):
    """Определяет вид треугольника и координаты его вершин.

    Возвращает кортеж (тип треугольника, список координат вершин).
    """
    logging.debug(f"Получены входные данные: a='{str_a}', b='{str_b}', c='{str_c}'")

    # Попытка преобразования входных строк в float
    try:
        a = float(str_a)
        b = float(str_b)
        c = float(str_c)
    except ValueError as ex:
        logging.error(f"Ошибка преобразования входных данных в числа: {ex}")
        logging.exception("Заход в блок обработки исключения:")
        return "", [(-2, -2)] * 3

    # Проверка на положительность
    if a <= 0 or b <= 0 or c <= 0:
        logging.error(f"Ошибочные числовые данные (стороны должны быть положительными): a={a}, b={b}, c={c}")
        return "не треугольник", [(-1, -1)] * 3

    # Проверка неравенства треугольника
    if a + b <= c or a + c <= b or b + c <= a:
        logging.error(f"Стороны a={a}, b={b}, c={c} не образуют треугольник (нарушено неравенство треугольника)")
        return "не треугольник", [(-1, -1)] * 3

    # Определение вида треугольника (с допуском на погрешность float)
    eps = 1e-9
    if abs(a - b) < eps and abs(b - c) < eps:
        triangle_type = "равносторонний"
    elif abs(a - b) < eps or abs(a - c) < eps or abs(b - c) < eps:
        triangle_type = "равнобедренный"
    else:
        triangle_type = "разносторонний"

    vertices = calculate_vertices(a, b, c)
    logging.info(f"Успешный запрос: a={a}, b={b}, c={c} -> тип='{triangle_type}', вершины={vertices}")
    return triangle_type, vertices


def read_side(prompt: str) -> str:
    """Читает одну сторону треугольника с клавиатуры."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым. Попробуйте снова.")


def main():
    setup_logger()

    while True:
        print("\n=== Вычисление вида треугольника ===")
        str_a = read_side("Введите длину стороны A: ")
        str_b = read_side("Введите длину стороны B: ")
        str_c = read_side("Введите длину стороны C: ")

        triangle_type, vertices = get_triangle_type(str_a, str_b, str_c)

        print(f"\nТип треугольника: {triangle_type}")
        print(f"Координаты вершин: {vertices}")

        again = input("\nПовторить? (д/н): ").strip().lower()
        if again not in ("д", "y", "yes", "да"):
            break

    logging.info("Приложение завершило работу")


if __name__ == "__main__":
    main()