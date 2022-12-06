class Counter:
    def __init__(self):
        self.cnt = 0
    def up(self):
        self.cnt += 1
    def down(self):
        self.cnt -= 1
    def clear(self):
        self.cnt = 0