from .validator import TriangleValidator

class TriangleController:
    def __init__(self, user_io, db, notifier, validator=None):
        self.user_io = user_io
        self.db = db
        self.notifier = notifier
        self.validator = validator or TriangleValidator

    def process(self):
        raw = self.user_io.get_triangle_sides()
        try:
            a, b, c = (float(x) for x in raw)
        except (TypeError, ValueError):
            result = {"sides": raw, "triangle_type": None, "error_message": "Длины сторон должны быть числами", "from_db": False}
            self.notifier.send(self._format_message(result))
            return result

        record = self.db.get_record(a, b, c)
        if record is not None:
            result = {"sides": (a, b, c), "triangle_type": record["triangle_type"], "error_message": record["error_message"], "from_db": True}
        else:
            triangle_type, error_message = self.validator.determine_type(a, b, c)
            self.db.add_record(a, b, c, triangle_type, error_message)
            result = {"sides": (a, b, c), "triangle_type": triangle_type, "error_message": error_message, "from_db": False}

        self.notifier.send(self._format_message(result))
        return result

    @staticmethod
    def _format_message(result):
        if result["error_message"]:
            return f"Стороны {result['sides']}: ошибка — {result['error_message']}"
        return f"Стороны {result['sides']}: тип — {result['triangle_type']}"