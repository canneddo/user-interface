from kivy.app import App
from lanedisplay import LaneDisplay
from lanesliders import LaneSliders
from lanecanvas import LaneCanvas
from gearshift import GearShift
from speedyawadjust import SpeedYawAdjust
from lanecenteringstatus import LaneCenteringStatus
from sliderinput import SliderInput
from inputhandler import InputHandler

input_handler = InputHandler()


class MockUIApp(App):
    def __init__(self, **kwargs):
        super(MockUIApp, self).__init__(**kwargs)
