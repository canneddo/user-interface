from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty

class SpeedYawAdjust(BoxLayout):
    speed = NumericProperty(0)
    yaw_rate = NumericProperty(0)

    def __init__(self, **kwargs):
        super(SpeedYawAdjust, self).__init__(**kwargs)
        print(self.children)

    def speed_update(self, speed):
        self.speed = speed

    def yaw_update(self, yaw_rate):
        self.yaw_rate = yaw_rate