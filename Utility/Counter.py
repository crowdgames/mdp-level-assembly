class Counter:
    def __init__(self):
        self.n = {}

    def add(self, name):
        if name in self.n:
            self.n[name] += 1
        else:
            self.n[name] = 1

    def get(self, name, default=0):
        if name in self.n:
            return self.n[name]
        
        return default