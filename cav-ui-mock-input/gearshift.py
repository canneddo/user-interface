from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, NumericProperty

class GearShift(BoxLayout):
    car_on = BooleanProperty(False)
    shifter_position = NumericProperty(0)

    car_on_button_text = ["Turn car on", "Turn car off"]
    button_colors = { 'red': [1, 0.2, 0, 1], 'green': [0, 1, 0, 1], 'default': [1, 1, 1, 1] }

    def __init__(self, **kwargs):
        super(GearShift, self).__init__(**kwargs)
        self.startCarButton = Button(text=self.car_on_button_text[0])
        self.startCarButton.background_color = self.button_colors['red']
        self.startCarButton.bind(on_press=self.on_press_start)
        self.add_widget(self.startCarButton)

    def on_press_start(self, _):
        if (self.car_on):
            self.startCarButton.background_color = self.button_colors['red']
            self.startCarButton.text = self.car_on_button_text[0]
            self.car_on = False
        else:
            self.startCarButton.background_color = self.button_colors['green']
            self.startCarButton.text = self.car_on_button_text[1]
            self.car_on = True

    def gear_button_press(self, gear, button):
        self.children[4 - self.shifter_position].background_color = self.button_colors['default']
        button.background_color = self.button_colors['green']
        self.shifter_position = gear