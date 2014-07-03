class RightDirection(object):
    def __init__(self, model, count):
        self.model = model
        self.count = count

    def move(self, window):
        (x, y, w, h) = self.model.geometry_for(window)
        self.model.move_window(window, x + self.count, y, w, h)
