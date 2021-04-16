from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Line

class LanePlot(BoxLayout):
    def __init__(self, **kwargs):
        super(LanePlot, self).__init__(**kwargs)
        with self.canvas:
            Line(points=[600,700,700,600], width=2)