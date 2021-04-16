from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

class SliderInput(BoxLayout):
    direction = StringProperty('horizontal')
    labelwidth = NumericProperty(50)
    sliderwidth = NumericProperty(50)
    textinputwidth = NumericProperty(50)
    labeltext = StringProperty()
    value = NumericProperty(0)
    value_min = NumericProperty(0)
    value_max = NumericProperty(10)
    step = NumericProperty(1)

    def __init__(self, **kwargs):
        super(SliderInput, self).__init__(orientation='horizontal',**kwargs)
        Clock.schedule_once(self.create_widgets, 0)

    def create_widgets(self, _):
        slider_params = { 'value': self.value, 'min': self.value_min, 'max': self.value_max, 'step': self.step }
        textinput_params = { 'halign': 'right', 'multiline': False, 'input_filter': 'float', 'unfocus_on_touch': True,
        'text': str(self.value)
        }
        label = Label(text=self.labeltext, size=(self.labelwidth, 25), size_hint=(None, None))
        self.slider = self.textinput = None
        if (self.direction == 'vertical'):
            self.height = 85; self.orientation = 'vertical'
            self.slider = Slider(**slider_params, height=30, size_hint_y=None)
            self.textinput = TextInput(**textinput_params, height=30, size_hint_x=1)
        elif (self.direction == 'horizontal'):
            self.slider = Slider(**slider_params)
            self.textinput = TextInput(**textinput_params, size=(self.textinputwidth, 30), size_hint=(None, None))
        self.slider.bind(value=self.slider_update)
        self.textinput.bind(focus=self.on_textinput_focus)
        self.add_widget(label); self.add_widget(self.slider); self.add_widget(self.textinput)

    def slider_update(self, _, value):
        self.value = round(value,5)
        self.textinput.text = str(self.value)

    def on_textinput_focus(self, textinput, focus):
        if (focus is True):
            return # not focus lose
        try:
            value = float(textinput.text)
            self.slider.value = value
            self.value = value
        except Exception:
            textinput.text = str(self.slider.value)