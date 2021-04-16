from kivy.uix.widget import Widget

class LaneCanvas(Widget):
    def __init__(self, **kwargs):
        super(LaneCanvas, self).__init__(**kwargs)
        with self.canvas:
            Line(points=[600,700,700,600], width=2)