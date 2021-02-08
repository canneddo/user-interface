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
image_paths = [join(curdir, 'images', image).replace('\\', '/') for image in ['third_wheel_icon.png',
'pngfind.com-phone-icon-png-1835900.png',
'pngfind.com-location-symbol-png-1655717.png',
'pngfind.com-bluetooth-png-1528441.png',
'pngfind.com-musical-note-png-254061.png',
'pngfind.com-radio-png-524979.png',
'pngfind.com-settings-icon-png-859089.png']]

# class BTN(Image):
#     def __init__(self, p, **kwargs):
#         super(BTN, self).__init__(**kwargs)
#         self.p = p

#     def on_touch_down(self, a):
#         print("click")
#         self.p('asd')

Builder.load_string("""
<CarHomeScreen>:
    # GridLayout:
    #     cols: 1
    #     size: root.width, root.height * 0.1
    #     Button:
    #         height: root.height * 0.1
    #         label: 'Shift out of Park'
    #         on_press: root.manager.current = 'dashboard'
    StackLayout:
        orientation: 'lr-tb'
        padding: 50
        spacing: 50
        Image:
            source: '{0}'
            size_hint: 0.2,0.2
            on_touch_down: root.manager.current = 'menu'
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
            on_press: root.manager.current = 'dashboard'
""".format(*image_paths))

class CarHomeScreen(Screen):
    pass
# class CarHomeScreen(Screen):
#     def __init__(self, sm, **kwargs):
#         super(CarHomeScreen, self).__init__(**kwargs)
#         stacklayout_args = {
#             'orientation': 'lr-tb',
#             'padding': 10,
#             'spacing': 10
#         }

#         curdir = dirname(__file__)
#         file_names = [join(curdir, 'images', image) for image in ['third_wheel_icon.png',
#         'pngfind.com-phone-icon-png-1835900.png',
#         'pngfind.com-location-symbol-png-1655717.png',
#         'pngfind.com-bluetooth-png-1528441.png',
#         'pngfind.com-musical-note-png-254061.png',
#         'pngfind.com-radio-png-524979.png',
#         'pngfind.com-settings-icon-png-859089.png']]

#         i_path = 'F:/Programming/user-interface/src/images/pngfind.com-musical-note-png-254061.png'
#         button_args = {
#             'width': 40 + 22 * 5,
#             'height': 40 + 22 * 5,
#             # 'background_color': (128,128,128, 0),
#             # 'background_normal': i_path
#             'on_press': self.btn_press
#         }

#         self.sm = sm
#         root = StackLayout(**stacklayout_args)
#         for i in range(len(file_names)):
#             btn = Button(size_hint=(None, None), background_normal=file_names[i], **button_args)
#             root.add_widget(btn)
#         root.add_widget(BTN(self.btn_press, source=file_names[0]))
#         self.add_widget(root)

#     def btn_press(self, a, **kwargs):
#         self.sm.current = 'menu'

class MyApp(App):

    def build(self):
        return CarHomeScreen()


if __name__ == '__main__':
    Window.size = ((40 + 22 * 5 + 10) * 5 + 10, 500)
    MyApp().run()