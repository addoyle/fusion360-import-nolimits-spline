class Spline:
    center = []
    left = []
    right = []

    def clear(self):
        self.center.clear()
        self.left.clear()
        self.right.clear()
    
    @property
    def count(self) -> int:
        return len(self.center)