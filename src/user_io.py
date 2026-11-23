from abc import ABC, abstractmethod

class BaseUserIO(ABC):
    @abstractmethod
    def get_triangle_sides(self):
        pass

class ConsoleUserIO(BaseUserIO):
    def get_triangle_sides(self):
        return (
            input("Введите сторону 1: "),
            input("Введите сторону 2: "),
            input("Введите сторону 3: ")
        )