# memory.py - إدارة الذاكرة (Memory Store)

class Memory:
    def __init__(self):
        self.history = []

    def add(self, message: str):
        self.history.append(message)

    def get_recent(self, n: int = 5):
        return self.history[-n:]
