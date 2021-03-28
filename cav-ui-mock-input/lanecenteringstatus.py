from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty

class LaneCenteringStatus(BoxLayout):
    lane_centering_status = NumericProperty(0)

    button_colors = { 'green': [0, 1, 0, 1], 'default': [1, 1, 1, 1] }

    def __init__(self, **kwargs):
        super(LaneCenteringStatus, self).__init__(**kwargs, orientation='vertical')

    def status_button_press(self, status, button):
        self.children[0].children[3 - self.lane_centering_status].background_color = self.button_colors['default']
        button.background_color = self.button_colors['green']
        self.lane_centering_status = status