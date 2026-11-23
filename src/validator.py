class TriangleValidator:
    @staticmethod
    def determine_type(a, b, c):
        try:
            a, b, c = float(a), float(b), float(c)
        except (TypeError, ValueError):
            return None, "Длины сторон должны быть числами"
        if a <= 0 or b <= 0 or c <= 0:
            return None, "Длины сторон должны быть положительными"
        if a + b <= c or a + c <= b or b + c <= a:
            return None, "Треугольник с такими сторонами не существует"
        if a == b == c:
            return "равносторонний", None
        if a == b or b == c or a == c:
            return "равнобедренный", None
        return "разносторонний", None