from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from sliderinput import SliderInput
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock

slider_input_params = [
    { 'value_min': -1e-4, 'value_max': 1e-4, 'step': 1e-5 },
    { 'value_min': -0.02, 'value_max': 0.02, 'step': 0.002 },
    { 'value_min': -0.35, 'value_max': 0.35, 'step': 0.05 },
    { 'value_min': -3, 'value_max': 3, 'step': 0.1 }
]
labels = [ 'Lane Curvature Derivative',
           'Lane Curvature',
           'Lane Heading',
           'Distance to Lane' ]
label_widths = [200, 130, 130, 150]

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
        if (slider.labeltext.endswith(labels[1])):
            index = 1
        elif (slider.labeltext.endswith(labels[2])):
            index = 2
        elif (slider.labeltext.endswith(labels[3])):
            index = 3
        self.lane_parameters[index] = value

    def add_widgets(self, _):
        self.children[-1].text = self.label
        for i in range(4):
            params = slider_input_params[i]
            labeltext = labels[i]
            slider = SliderInput(**params, labeltext=labeltext, labelwidth=label_widths[i], direction='vertical')
            slider.bind(value=self.on_update_slider_input)
            self.add_widget(slider)
            self.add_widget(Widget())