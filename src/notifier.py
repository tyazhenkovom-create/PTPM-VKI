from abc import ABC, abstractmethod

class BaseNotifier(ABC):
    @abstractmethod
    def send(self, message):
        pass

class ConsoleNotifier(BaseNotifier):
    def __init__(self):
        self.sent_messages = []

    def send(self, message):
        self.sent_messages.append(message)
        print(f"[NOTIFIER] Отправлено: {message}")
        return True