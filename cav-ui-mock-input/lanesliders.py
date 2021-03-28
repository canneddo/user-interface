from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from sliderinput import SliderInput
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock

slider_input_params = [
    { 'value_min': -1.2e-4, 'value_max': 1.2e-4, 'step': 1e-6 },
    { 'value_min': -0.02, 'value_max': 0.02, 'step': 0.001 },
    { 'value_min': -0.357, 'value_max': 0.357, 'step': 0.001 },
    { 'value_min': -127, 'value_max': 128 }
]
labels = [ 'lane_curvature_derivative', 
           'lane_curvature', 
           'lane_heading', 
           'distance_to_lane' ]

class LaneSliders(BoxLayout):
    label =  StringProperty()
    lane_name = StringProperty()
    lane_parameters = ListProperty([0, 0, 0, 0])

    def __init__(self, **kwargs):
        super(LaneSliders, self).__init__(orientation='vertical', **kwargs)
        self.add_widget(Label(height=25, size_hint_y=None))
        Clock.schedule_once(self.add_widgets, 0)

    def on_update_slider_input(self, slider, value):
        index = 0
        if (slider.labeltext.endswith('lane_curvature')):
            index = 1
        elif (slider.labeltext.endswith('lane_heading')):
            index = 2
        elif (slider.labeltext.endswith('distance_to_lane')):
            index = 3
        self.lane_parameters[index] = value

    def add_widgets(self, _):
        self.children[-1].text = self.label
        for i in range(4):
            params = slider_input_params[i]
            labeltext = self.lane_name + labels[i]
            slider = SliderInput(**params, labeltext=labeltext, labelwidth= 120, direction='vertical')
            slider.bind(value=self.on_update_slider_input)
            self.add_widget(slider)
            self.add_widget(Widget())