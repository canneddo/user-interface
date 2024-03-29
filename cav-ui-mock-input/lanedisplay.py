from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty

class LaneDisplay(BoxLayout):
    left_lane_detected = BooleanProperty(False)
    right_lane_detected = BooleanProperty(False)

    lane_centering_button_text = ['{} left lane\nilc_laneLeftDetected', '{} right lane\nilc_laneLeftDetected']
    lane_display_button_text = ["Turn car on", "Turn car off"]
    button_colors = { 'green': [0, 1, 0, 1], 'default': [1, 1, 1, 1] }

    def __init__(self, **kwargs):
        super(LaneDisplay, self).__init__(**kwargs, orientation='vertical')

    def lane_detector_press(self, lane, button):
        lane_property = ''
        button_text = ''

        if (lane == 0):
            button_text = self.lane_centering_button_text[0]
            lane_property = 'left_lane_detected'
        else:
            button_text = self.lane_centering_button_text[1]
            lane_property = 'right_lane_detected'

        if (getattr(self, lane_property)):
            button.background_color = self.button_colors['default']
            button.text = button_text.format('Detect')
            setattr(self, lane_property, False)
        else:
            button.text = button_text.format('Un-detect')
            button.background_color = self.button_colors['green']
            setattr(self, lane_property, True)