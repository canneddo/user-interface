from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
import io
from os.path import dirname, join
from kivy.lang import Builder

curdir = dirname(__file__)
image_paths = [join(curdir, '../images', image).replace('\\', '/') for image in ['third_wheel_icon.png',
'pngfind.com-phone-icon-png-1835900.png',
'pngfind.com-location-symbol-png-1655717.png',
'pngfind.com-bluetooth-png-1528441.png',
'pngfind.com-musical-note-png-254061.png',
'pngfind.com-radio-png-524979.png',
'pngfind.com-settings-icon-png-859089.png']]

Builder.load_string("""
<CarHomeScreen>:
    StackLayout:
        orientation: 'lr-tb'
        padding: 50
        spacing: 50
        Image:
            source: '{0}'
            size_hint: 0.2,0.2
            on_touch_down: 
                app.playButtonTone()
                root.manager.transition.direction = 'left'
                root.manager.current = 'menu'
        Image:
            source: '{1}'
            size_hint: 0.2,0.2
        Image:
            source: '{2}'
            size_hint: 0.2,0.2
        Image:
            source: '{3}'
            size_hint: 0.2,0.2
        Image:
            source: '{4}'
            size_hint: 0.2,0.2
        Image:
            source: '{5}'
            size_hint: 0.2,0.2
        Image:
            source: '{6}'
            size_hint: 0.2,0.2
        Button:
            size_hint: 0.2,0.2
            text: 'Shift out of Park'
            on_press:
                app.playButtonTone()
                root.manager.transition.direction = 'right' 
                root.manager.current = 'dashboard'
""".format(*image_paths))

class CarHomeScreen(Screen):
    pass

# class MyApp(App):

#     def build(self):
#         return CarHomeScreen()


# if __name__ == '__main__':
#     Window.size = ((40 + 22 * 5 + 10) * 5 + 10, 500)
#     MyApp().run()